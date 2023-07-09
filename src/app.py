#!/usr/bin/env python
# -*- coding: utf-8 -*-

import streamlit as st
from datetime import date
from typing import Any
import requests
import pandas as pd
from streamlit_lottie import st_lottie

import plotly.express as px
import plotly.graph_objects as go

# from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
# from htbuilder.units import percent, px
# from htbuilder.funcs import rgba, rgb


# def image(src_as_string, **style):
#     return img(src=src_as_string, style=styles(**style))


# def link(link, text, **style):
#     return a(_href=link, _target="_blank", style=styles(**style))(text)


# def layout(*args):

#     style = """
#     <style>
#       # MainMenu {visibility: hidden;}
#       footer {visibility: hidden;}
#      .stApp { bottom: 105px; }
#     </style>
#     """

## global variables

today = date.today().strftime("%Y-%m-%d")

apiVersion = "1"

plotly_theme = "ggplot2"

gif_url = "https://assets10.lottiefiles.com/packages/lf20_ystsffqy.json"

st.set_page_config(layout="wide")

## Get data from API


def get_currencies(date=today) -> Any:
    currency_url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@{apiVersion}/{date}/currencies.json"
    return requests.get(currency_url).json()


def get_exchange_rates(date=today) -> Any:
    exchange_url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@{apiVersion}/{date}/currencies/eur.json"
    return requests.get(exchange_url).json()


def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()


currency_names = get_currencies(date="latest")
exchange_rates = get_exchange_rates(date="latest")

st_lottie(load_lottie_url(gif_url), speed=1, height=100, key="initial")

st.markdown("# What is your level of millionaire?")


col1, col2 = st.columns(2)

with col1:
    wealth = st.number_input("How much money do you have?", value=10000, step=1000)
with col2:
    currency = st.selectbox("In which currency?", list(currency_names.keys()))

# st.write(exchange_rates)
wealth_in_eur = wealth / exchange_rates["eur"][currency]

wealth_in_currencies = [
    {
        "currency_code": currency,
        "currency": currency_names[currency],
        "amount": wealth_in_eur * exchange_rates["eur"][currency],
    }
    for currency in currency_names.keys()
]

df = pd.DataFrame.from_records(wealth_in_currencies)
df = df.query("currency != ''")
df.sort_values(by="amount", ascending=False, inplace=True)
# st.write(df)

st.divider()

## Ratio of currencies in which you are a millionaire
st.markdown("## Millionaire ratio")

df["millionaire"] = df["amount"] > 1e6
df["unit"] = 1

plot_col1, plot_col2 = st.columns(2)

with plot_col1:
    # st.write(df)
    st.caption(
        "Here are the top 5 currencies in which your wealth is pretty close to reach 1 million."
    )
    close_ones = df.query("amount < 1e6")[["amount", "currency"]].head(5)
    fig = px.bar(
        close_ones,
        x="currency",
        y="amount",
        title="Closest ones",
        template=plotly_theme,
        width=400,
    )  # height=400)
    st.plotly_chart(fig, use_container_width=True)

with plot_col2:
    st.caption(
        f"As of {exchange_rates['date']} there are {len(df)} currencies and cryptos to compare to in this site and you are a millionaire in {df['millionaire'].sum()} of them."
    )

    fig = px.pie(
        df,
        values="unit",
        names="millionaire",
        title="Millionaire?",
        template=plotly_theme,
        width=400,
    )  # height=400
    st.plotly_chart(fig, use_container_width=True)

# st.bar_chart(df, x="currency", y="amount")


st.divider()

st.markdown("## Major currencies")

st.caption(
    "Here you can see your wealth in major currencies and check how much you need to be a millionaire in each of them."
)

no_margin_layout = go.Layout(
    margin=go.layout.Margin(
        l=0, r=0, b=0, t=0  # left margin  # right margin  # bottom margin  # top margin
    )
)

benchmark_cols = st.columns(5)

with benchmark_cols[0]:
    eur_fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=wealth_in_eur,
            delta={"position": "top", "reference": 1_000_000},
            title={"text": "EUR"},
            domain={"x": [0, 1], "y": [0, 1]},
        ),
        layout=no_margin_layout,
    )

    st.plotly_chart(eur_fig, use_container_width=True)

with benchmark_cols[1]:
    usd_fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=wealth_in_eur * exchange_rates["eur"]["usd"],
            delta={"position": "top", "reference": 1_000_000},
            title={"text": "USD"},
            domain={"x": [0, 1], "y": [0, 1]},
        ),
        layout=no_margin_layout,
    )

    st.plotly_chart(usd_fig, use_container_width=True)

with benchmark_cols[2]:
    jpy_fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=wealth_in_eur * exchange_rates["eur"]["jpy"],
            delta={"position": "top", "reference": 1_000_000},
            title={"text": "JPY"},
            domain={"x": [0, 1], "y": [0, 1]},
        ),
        layout=no_margin_layout,
    )

    st.plotly_chart(jpy_fig, use_container_width=True)

with benchmark_cols[3]:
    aud_fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=wealth_in_eur * exchange_rates["eur"]["aud"],
            delta={"position": "top", "reference": 1_000_000},
            title={"text": "AUD"},
            domain={"x": [0, 1], "y": [0, 1]},
        ),
        layout=no_margin_layout,
    )

    st.plotly_chart(aud_fig, use_container_width=True)

with benchmark_cols[4]:
    eth_fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=wealth_in_eur * exchange_rates["eur"]["eth"],
            delta={"position": "top", "reference": 1_000_000},
            title={"text": "ETH"},
            domain={"x": [0, 1], "y": [0, 1]},
        ),
        layout=no_margin_layout,
    )

    st.plotly_chart(eth_fig, use_container_width=True)

st.divider()
