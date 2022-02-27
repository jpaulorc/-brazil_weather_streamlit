import csv
import itertools
from pathlib import Path

import pandas as pd
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
    def __init__(self, fraction: float) -> None:
        self.stations = Stations()
        self.weather_df = self.get_sample_weather(fraction)

    def asfloat_inplace(self, df: pd.DataFrame, columns: list):
        for col in columns:
            if df[col].dtype in [object, str]:
                df[col] = df[col].str.replace(",", ".").astype(float)
        return df

    def get_sample_weather(self, sample: float):
        stations_df = self.stations.stations_unification()

        all_cities_df = []
        for filename in INPUT_PATH.iterdir():
            current_df = pd.read_csv(filename, sep=";", header=9)

            with open(filename, "r") as file:
                csv_file = csv.reader(file, delimiter=";")
                header_list = [i for i in itertools.islice(csv_file, 9)]
                current_df["station"] = ".".join(map(str, header_list[1])).split(": ")[1]
                all_cities_df.append(current_df)
                file.close()

        df = pd.concat(all_cities_df)
        df.rename(columns=COLUMNS, inplace=True)
        df.drop("Unnamed: 11", axis=1, inplace=True)

        df = pd.merge(
            left=df,
            right=stations_df,
            left_on="station",
            right_on="station",
        )

        df = self.asfloat_inplace(df, COL_NUMBERS)
        return df.sample(frac=sample / 100, replace=True, random_state=1)

    def get_unique_regions(self):
        return self.weather_df.region.unique()
