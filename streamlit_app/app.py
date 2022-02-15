"""import csv
import glob
import itertools
import os
import random

import altair as alt
import bar_chart_race as bcr
import folium
import matplotlib.patches as mpatches
import missingno as msno
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import requests
import pandas as pd"""

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
from weather import Weather

# from branca.element import Figure

st.set_page_config(layout="wide")


def display_header():

    row0_0, row0_1 = st.columns((2, 1))

    with row0_0:
        st.title("Brazil Data Meteorological Visualization")
        st.markdown(
            "[![GitHub](https://badgen.net/badge/icon/GitHub?icon=github&color=black&label)](https://github.com/jpaulorc/brazil_weather_streamlit)"
        )
    with row0_1:
        st.subheader(
            "Project created to obtain information about the weather in Brazil, from 2000 to 2020."
        )

    st.markdown("---")

    row1_0, row1_1, row1_2 = st.columns((3, 1, 2))

    with row1_0:
        st.markdown(
            """
                ### Data collected by [INMET](https://portal.inmet.gov.br/): National Institute of Meteorology.
            """
        )
        # st.image(Image.open("img/INMET.png"))

    row1_2.markdown(
        """
        ### Datasets:

        [Complete Brazil Weather Database - 2000/2020](https://www.kaggle.com/gbofrc/complete-brazil-weather-database-20002020)

        Data collected by meteorological stations of the National Institute of Meteorology - INMET, distributed in the Brazilian territory between 2000 and 2021.

        [INMET Automatic Stations](https://portal.inmet.gov.br/paginas/catalogoaut)

        Location from INMET weather stations.
        """
    )

    st.markdown("---")

    weather = Weather(0.1)

    row2_0, row2_1 = st.columns(2)

    with row2_0:
        df = weather.get_stations_location()

        fig, ax = plt.subplots()
        sns.set_theme(style="whitegrid")
        stations = sns.lmplot(
            x="longitude",
            y="latitude",
            data=df,
            fit_reg=False,
            legend=False,
            scatter_kws={"s": 30},
            hue="region",
            height=10,
        )

        stations.set(xlabel="Longitude", ylabel="Latitude")
        stations.fig.suptitle("Station's Location", fontsize=20)
        stations.fig.legend(
            labels=weather.get_unique_regions(), loc="center right", title="Region"
        )

        # plt.show()

        st.write(fig)


display_header()
