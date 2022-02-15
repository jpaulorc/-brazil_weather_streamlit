"""import csv
import glob
import itertools
import os
import random

import altair as alt
import bar_chart_race as bcr
import folium
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import missingno as msno
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import requests
import seaborn as sns
import pandas as pd"""

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

    weather = Weather()
    weather.save_sample()


display_header()
