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
UF = {
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
REGION = {
    "region": ["N", "NE", "CO", "SE", "S"],
    "name": ["Norte", "Nordeste", "Centro Oeste", "Sudeste", "Sul"],
}


class Stations:
    def stations_unification(self):
        stations_df = pd.read_csv(
            filepath_or_buffer=STATION_FILENAME,
            sep=";",
            usecols=USECOLS,
        )
        stations_df.rename(columns=COLUMNS_NAME, inplace=True)
        region_df = pd.DataFrame(UF)

        stations_df = pd.merge(left=stations_df, right=region_df, left_on="uf", right_on="uf")
        stations_df = pd.merge(
            left=stations_df, right=pd.DataFrame(REGION), left_on="region", right_on="region"
        )

        return stations_df

    def asfloat_inplace(self, df: pd.DataFrame, columns: list):
        for col in columns:
            if df[col].dtype in [object, str]:
                df[col] = df[col].str.replace(",", ".").astype(float)
        return df
