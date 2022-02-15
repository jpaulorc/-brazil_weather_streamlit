import pandas as pd

STATION_FILENAME = "data/CatalogoEstacoesAutomaticas.csv"
USECOLS = [
    "SG_ESTADO",
    "DC_NOME",
    "CD_ESTACAO",
    "VL_LATITUDE",
    "VL_LONGITUDE",
    "VL_ALTITUDE",
]
COLUMNS_NAME = {
    "SG_ESTADO": "uf",
    "DC_NOME": "cityname",
    "CD_ESTACAO": "station",
    "VL_LATITUDE": "latitude",
    "VL_LONGITUDE": "longitude",
    "VL_ALTITUDE": "altitude",
}
REGION = {
    "region": [
        "N",
        "N",
        "N",
        "N",
        "N",
        "N",
        "N",
        "NE",
        "NE",
        "NE",
        "NE",
        "NE",
        "NE",
        "NE",
        "NE",
        "NE",
        "CO",
        "CO",
        "CO",
        "CO",
        "SE",
        "SE",
        "SE",
        "SE",
        "S",
        "S",
        "S",
    ],
    "uf": [
        "AM",
        "RR",
        "AP",
        "PA",
        "TO",
        "RO",
        "AC",
        "MA",
        "PI",
        "CE",
        "RN",
        "PE",
        "PB",
        "SE",
        "AL",
        "BA",
        "MT",
        "MS",
        "GO",
        "DF",
        "SP",
        "RJ",
        "ES",
        "MG",
        "PR",
        "RS",
        "SC",
    ],
}


class Stations:
    def stations_unification(self):
        stations_df = pd.read_csv(
            filepath_or_buffer=STATION_FILENAME,
            sep=";",
            usecols=USECOLS,
        )
        stations_df.rename(columns=COLUMNS_NAME, inplace=True)
        region_df = pd.DataFrame(REGION)

        return pd.merge(left=stations_df, right=region_df, left_on="uf", right_on="uf")
