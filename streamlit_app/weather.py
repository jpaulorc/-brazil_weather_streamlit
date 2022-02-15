import csv
import glob
import itertools
import os
from pathlib import Path

import pandas as pd
import streamlit as st
from stations import Stations

# PATH = "data/brazil_weather/"
# WEATHER_FILE_NAME = "data/brazil_weather/weather.csv"

INPUT_PATH = Path("data/brazil_weather/")
OUTPUT_PATH = Path("data/")

FILE_EXTENSION = ".csv"
COLUMNS = {
    "Data Medicao": "date",
    "PRECIPITACAO TOTAL, DIARIO (AUT)(mm)": "tot_precipitation",
    "PRESSAO ATMOSFERICA MEDIA DIARIA (AUT)(mB)": "avg_atm_pressure",
    "TEMPERATURA DO PONTO DE ORVALHO MEDIA DIARIA (AUT)(°C)": "avg_dew_temp",
    "TEMPERATURA MAXIMA, DIARIA (AUT)(°C)": "max_temp",
    "TEMPERATURA MEDIA, DIARIA (AUT)(°C)": "avg_temp",
    "TEMPERATURA MINIMA, DIARIA (AUT)(°C)": "min_temp",
    "UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)": "avg_rel_humidity",
    "UMIDADE RELATIVA DO AR, MINIMA DIARIA (AUT)(%)": "min_rel_humidity",
    "VENTO, RAJADA MAXIMA DIARIA (AUT)(m/s)": "max_blast_wind",
    "VENTO, VELOCIDADE MEDIA DIARIA (AUT)(m/s)": "avg_vel_wind",
}
COL_NUMBERS = [
    "tot_precipitation",
    "avg_atm_pressure",
    "avg_dew_temp",
    "max_temp",
    "avg_temp",
    "min_temp",
    "avg_rel_humidity",
    "min_rel_humidity",
    "max_blast_wind",
    "avg_vel_wind",
    "latitude",
    "longitude",
    "altitude",
]


class Weather:
    def __init__(self) -> None:
        self.stations = Stations()

    def asfloat_inplace(self, df: pd.DataFrame, columns: list):
        for col in columns:
            if df[col].dtype in [object, str]:
                df[col] = df[col].str.replace(",", ".").astype(float)

    def save_sample(self):
        for filename in INPUT_PATH.iterdir():
            # all_filenames = enumerate([i for i in glob.glob(f"*{FILE_EXTENSION}")])
            # st.markdown(filename)

            all_cities_df = []

            """for index, row in all_filenames:
                filename = PATH + row"""

            current_df = pd.read_csv(filename, sep=";", header=9)

            with open(filename, "r") as file:
                csv_file = csv.reader(file, delimiter=";")
                header_list = [i for i in itertools.islice(csv_file, 9)]
                current_df["station"] = ".".join(map(str, header_list[1])).split(": ")[1]
                all_cities_df.append(current_df)
                file.close()

        weather_df = pd.concat(all_cities_df)
        weather_df.rename(columns=COLUMNS, inplace=True)
        weather_df.drop("Unnamed: 11", axis=1, inplace=True)

        weather_df = pd.merge(
            left=weather_df,
            right=self.stations.stations_unification(),
            left_on="station",
            right_on="station",
        )

        self.asfloat_inplace(weather_df, COL_NUMBERS)
        weather_df.to_csv(OUTPUT_PATH.joinpath(f"weather{FILE_EXTENSION}"), index=False)
