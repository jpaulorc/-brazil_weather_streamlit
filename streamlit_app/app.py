import csv
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
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import seaborn as sns
import streamlit as st
from branca.element import Figure


def display_header():
    """Used to display the header"""
    st.title("Brazil Weather Data Visualization")
    st.text("Brazil Weather Data Visualization")
    st


display_header()
