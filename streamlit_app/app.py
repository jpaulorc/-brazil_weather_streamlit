import bar_chart_race as bcr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
import streamlit.components.v1 as components
from stations import Stations
from weather import Weather

KAGGLE_URL = "https://www.kaggle.com/gbofrc/complete-brazil-weather-database-20002020"
STATIONS_URL = "https://portal.inmet.gov.br/paginas/catalogoaut"

GITHUB_BADGE = "https://badgen.net/badge/icon/GitHub?icon=github&color=black&label"
GITHUB_LINK = "https://github.com/jpaulorc/brazil_weather_streamlit"
INMET_URL = "https://portal.inmet.gov.br/"

REGION = {"N": "North", "NE": "North East", "CO": "Midwest", "SE": "South East", "S": "South"}

st.set_page_config(layout="wide")


def display_header():

    row0_0, row0_1 = st.columns((2, 1))

    with row0_0:
        st.title("Brazil Data Meteorological Visualization")
        st.markdown(f"[![GitHub]({GITHUB_BADGE})]({GITHUB_LINK})")
    with row0_1:
        st.subheader(
            "Project created to obtain information about the weather in Brazil, from 2000 to 2020."
        )

    st.markdown("---")

    row1_0, row1_1, row1_2 = st.columns((3, 1, 2))

    with row1_0:
        st.markdown(
            f" ### Data collected by [INMET]({INMET_URL}) National Institute of Meteorology"
        )
        st.markdown("---")
        st.markdown("#### Choose the sample size:")
        sample_size = st.slider("Sample size (percentage)", 5, 100, step=5)  # min, max, default

    with row1_2:
        st.markdown(" ### Datasets:")
        st.markdown(f" [Complete Brazil Weather Database - 2000/2020]({KAGGLE_URL})")
        st.write(
            """Data collected by meteorological stations of the National Institute of Meteorology - INMET,
            distributed in the Brazilian territory between 2000 and 2021."""
        )
        st.markdown(f"[INMET Automatic Stations]({STATIONS_URL})")
        st.write("Location from INMET weather stations.")

    st.markdown("---")

    return sample_size


def stations_location():
    stations = Stations()
    df = stations.asfloat_inplace(
        stations.stations_unification(), ["latitude", "longitude", "altitude"]
    )
    st.subheader("Station's Location")

    row2_0, row2_1 = st.columns(2)

    with row2_0:
        st.markdown(
            """
            ### Identification of the analyzed places.

            According to the Latitude and Longitude information we can identify the location of
            the weather measuring stations on Brazil's map.
            """
        )

    with row2_1:

        df = df.drop(df.columns.difference(["longitude", "latitude", "region", "name"]), axis=1)
        df = df.loc[df["latitude"] > -40]

        fig = sns.lmplot(
            x="longitude",
            y="latitude",
            data=df,
            fit_reg=False,
            legend=False,
            scatter_kws={"s": 30},
            hue="region",
            height=10,
        )

        fig.set(xlabel="Longitude", ylabel="Latitude")
        fig.fig.suptitle("Station's Location", fontsize=20)
        fig.fig.legend(labels=df.name.unique(), loc="upper right", title="Region")

        with st.spinner("Little more... Plotting the results..."):
            st.pyplot(fig)


def get_sample(sample_size):
    with st.spinner("Little more... Getting the sample data..."):
        weather = Weather(sample_size)
    return weather.weather_df


def set_plot_title(title):
    st.markdown("---")
    st.markdown(f"### {title}")


def set_plot_description(description):
    st.markdown(f"{description}")


def plot_corretation(weather_df):
    set_plot_title("Correlation Analysis.")
    set_plot_description(
        """
        Heatmap display plotting the correlation between the columns. Also, the repetition will
        be removed by plotting only the elements on the lower diagonal.
        The graph will only display values for correlations less than -0.25 and greater than 0.25.
        """
    )

    with st.spinner("Little more... Working on the data..."):
        df = weather_df.loc[
            :,
            [
                "tot_precipitation",
                "avg_atm_pressure",
                "avg_dew_temp",
                "max_temp",
                "avg_temp",
                "min_temp",
                "avg_rel_humidity",
                "max_blast_wind",
                "avg_vel_wind",
                "altitude",
            ],
        ]

        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

        df = df.corr()
        df = df.iloc[1:, :-1]

        mask = np.triu(np.ones_like(df), k=1)

        plt.figure(figsize=(20, 10))

        x_axis_labels = [
            "Precipitation (Tot)",
            "Atm Pressure (Mean)",
            "Dew Temp (Mean)",
            "Temp (Max)",
            "Temp (Mean)",
            "Temp (Min)",
            "Relative Humidity (Mean)",
            "Wind Gust (Max)",
            "Wind (Mean Vel)",
        ]

        y_axis_labels = [
            "Atm Pressure (Mean)",
            "Dew Temp (Mean)",
            "Temp (Max)",
            "Temp (Mean)",
            "Temp (Min)",
            "Relative Humidity (Mean)",
            "Wind Gust (Max)",
            "Wind (Mean Vel)",
            "Latitude",
        ]

        ax = sns.heatmap(
            df,
            vmin=-1,
            vmax=1,
            cbar=False,
            cmap="coolwarm",
            mask=mask,
            annot=True,
            xticklabels=x_axis_labels,
            yticklabels=y_axis_labels,
        )

        for text in ax.texts:
            value = float(text.get_text())
            if -0.25 < value < 0.25:
                text.set_text("")
            else:
                text.set_text(round(value, 2))
            text.set_fontsize("12")

        plt.xticks(rotation=45, size="12")
        plt.yticks(size="12")
    with st.spinner("Little more... Plotting the results..."):
        st.pyplot(plt)


def get_region_dataframe():
    region = {
        "region": ["N", "NE", "CO", "SE", "S"],
        "region_name": ["North", "North East", "Midwest", "Southeast", "South"],
    }
    return pd.DataFrame(region)


def set_weather_by_region(weather_df):
    with st.spinner("Little more... Working on the data..."):
        df = weather_df.loc[:, ["max_temp", "date", "region"]]
        df.dropna(inplace=True)
        df["month"] = pd.DatetimeIndex(df["date"]).month
        df = pd.merge(left=df, right=get_region_dataframe(), left_on="region", right_on="region")
        df = df.sort_values(by=["month"])

    return df


def plot_brazil_max_temp(df):
    set_plot_title("Maximum Temperature Variation in Brazil (per month)")
    set_plot_description(
        """
        We can see that the maximum temperature in Brazil reaches its highest
        value between the months of October and February. However, if we consider
        each region of Brazil, we can see that the highest temperature is
        reached in different months of the year.
        """
    )

    plt.figure()

    with st.spinner("Little more... Plotting the results..."):
        sns.set(rc={"figure.figsize": (13, 9)})
        ax = sns.lineplot(y="max_temp", x="month", data=df)
        ax.set(
            xlabel="Mês",
            ylabel="Temperature (Maximum)",
            title="Maximum Temperature Variation in Brazil",
        )
        st.pyplot(plt)


def plot_brazil_regions_max_temp(df):
    set_plot_title("Maximum temperature variation by regions of Brazil.")

    plt.figure()
    with st.spinner("Little more... Plotting the results..."):
        g = sns.relplot(
            data=df,
            x="month",
            y="max_temp",
            col="region_name",
            height=4,
            aspect=0.7,
            kind="line",
        )
        (
            g.map(plt.axhline, y=0, color=".7", dashes=(2, 1), zorder=0)
            .set_axis_labels("Mês", "Temperature (Maximum)")
            .set_titles("Região: {col_name}")
            .tight_layout(w_pad=0)
        )
        st.pyplot(plt)

    plt.figure()
    with st.spinner("Little more... Plotting the results..."):
        sns.set(rc={"figure.figsize": (13, 9)})
        ax = sns.lineplot(y="max_temp", x="month", data=df, hue="region_name")
        ax.set(
            xlabel="Mês",
            ylabel="Temperature (Maximum)",
            title="Maximum temperature variation by regions of Brazil",
        )
        ax.legend().set_title("")
        st.pyplot(plt)


def plot_variables_byregion(weather_df):
    set_plot_title("Variables by region (Average)")
    set_plot_description(
        """
        Checking the average of some variables, we can see that there are large
        variations by region. An example is the average exclusion in the
        Northeast region is considerably lower than in other regions.
        """
    )

    with st.spinner("Little more... Working on the data..."):
        df = weather_df.loc[
            :,
            [
                "tot_precipitation",
                "avg_atm_pressure",
                "avg_dew_temp",
                "avg_temp",
                "avg_rel_humidity",
                "altitude",
                "region",
            ],
        ]
        df.dropna(inplace=True)

        columns = {
            "tot_precipitation": "Precipitation (Total)",
            "avg_atm_pressure": "Atmospheric Pressure (Average)",
            "avg_dew_temp": "Dew Temperature (Average)",
            "avg_temp": "Temperature (Average)",
            "avg_rel_humidity": "Relative Humidity (Average)",
            "altitude": "Altitude",
        }

        df.rename(columns=columns, inplace=True)
        df = pd.merge(left=df, right=get_region_dataframe(), left_on="region", right_on="region")

        df = df.groupby(["region_name"]).mean()
        df.reset_index(level=0, inplace=True)

        regions = df.region_name.unique()

    with st.spinner("Little more... Plotting the results..."):
        fig = go.Figure(
            data=[
                go.Bar(
                    name="Precipitation",
                    x=regions,
                    y=df["Precipitation (Total)"],
                    yaxis="y",
                    offsetgroup=1,
                ),
                go.Bar(
                    name="Atmospheric Pressure",
                    x=regions,
                    y=df["Atmospheric Pressure (Average)"],
                    yaxis="y2",
                    offsetgroup=2,
                ),
                go.Bar(
                    name="Dew Temperature",
                    x=regions,
                    y=df["Dew Temperature (Average)"],
                    yaxis="y3",
                    offsetgroup=3,
                ),
                go.Bar(
                    name="Temperature",
                    x=regions,
                    y=df["Temperature (Average)"],
                    yaxis="y4",
                    offsetgroup=4,
                ),
                go.Bar(
                    name="Relative Humidity",
                    x=regions,
                    y=df["Relative Humidity (Average)"],
                    yaxis="y5",
                    offsetgroup=5,
                ),
            ],
            layout={
                "yaxis": {
                    "title": "",
                    "visible": False,
                    "showticklabels": False,
                },
                "yaxis2": {
                    "title": "",
                    "overlaying": "y",
                    "side": "right",
                    "visible": False,
                    "showticklabels": False,
                },
                "yaxis3": {
                    "title": "",
                    "overlaying": "y",
                    "side": "right",
                    "visible": False,
                    "showticklabels": False,
                },
                "yaxis4": {
                    "title": "",
                    "overlaying": "y",
                    "side": "right",
                    "visible": False,
                    "showticklabels": False,
                },
                "yaxis5": {
                    "title": "",
                    "overlaying": "y",
                    "side": "right",
                    "visible": False,
                    "showticklabels": False,
                },
            },
        )

        fig.update_layout(barmode="group")
        st.plotly_chart(fig, use_container_width=True)


def set_air_humidity_byregion(weather_df):
    with st.spinner("Little more... Working on the data..."):
        df = weather_df.loc[:, ["date", "avg_rel_humidity", "region", "uf"]]
        df.dropna(inplace=True)
        df = pd.merge(left=df, right=get_region_dataframe(), left_on="region", right_on="region")

        return df.sample(10000)


def plot_air_humidity_byregion(df):
    set_plot_title("Variation of Relative Air Humidity (Average)")

    st.markdown("#### by Region")

    set_plot_description(
        """
        We can observe that the North region has a smaller interquartile range
        than the other regions. We also see that the minimum value is quite
        high when compared to other regions. Which generates a large range of outliers.
        """
    )

    with st.spinner("Little more... Plotting the results..."):
        fig = go.Figure()

        fig.add_trace(go.Box(x=df["region_name"], y=df["avg_rel_humidity"], notched=False))

        fig.update_layout(boxmode="group")
        st.plotly_chart(fig, use_container_width=True)


def get_region_name(region_code):
    return REGION[region_code]


def plot_air_humidity_selected_region(df, region_code):
    set_plot_title("Variation of Relative Air Humidity (Average)")
    st.markdown(f"#### Region: {get_region_name(region_code)}")

    with st.spinner("Little more... Plotting the results..."):
        fig = go.Figure()

        df = df.loc[df["region"] == region_code, :]

        fig = go.Figure()

        fig.add_trace(go.Box(x=df["uf"], y=df["avg_rel_humidity"], notched=False))

        fig.update_layout(boxmode="group")
        st.plotly_chart(fig, use_container_width=True)


def set_accumulated_rainfall(weather_df):
    with st.spinner("Little more... Working on the data..."):
        df = weather_df.loc[:, ["date", "tot_precipitation", "region", "uf"]]
        df.dropna(inplace=True)
        df = df.sample(10000)

        df["year_month"] = pd.to_datetime(df["date"]).dt.to_period("M")
        df = pd.merge(left=df, right=get_region_dataframe(), left_on="region", right_on="region")

        return df.sort_values(by=["year_month"])


def get_data_toplot(df, columns):
    with st.spinner("Little more... Working on the data..."):
        df = df.pivot_table(values="tot_precipitation", index=["year_month"], columns=columns)
        df = df.fillna(0)
        df.sort_values(list(df.columns), inplace=True)
        df = df.sort_index()
        df.iloc[:, 0:-1] = df.iloc[:, 0:-1].cumsum()
        top_rainning = set()
        for index, row in df.iterrows():
            top_rainning |= set(row[row > 0].sort_values(ascending=False).index)

        return df[top_rainning]


def plot_race_chart(df, title, height, sort="desc"):
    components.html(
        bcr.bar_chart_race(
            df=df,
            sort=sort,
            title=title,
        ).data,
        height=height,
    )


def plot_rainfall_byregion(df):
    set_plot_title("Accumulated rainfall in Brazil")
    st.markdown("#### by Region")

    with st.spinner("Little more... Plotting the results by Region..."):
        region_df = get_data_toplot(df, "region_name")
        plot_race_chart(region_df, "Accumulated rainfall by Regions of Brazil", 500, sort="desc")


def plot_rainfall_bystate(df, region_code):
    set_plot_title("Accumulated rainfall in Brazil")
    st.markdown(f"#### by States of {get_region_name(region_code)}")

    with st.spinner("Little more... Plotting the results by State..."):
        uf_df = get_data_toplot(df.loc[df["region"].isin([region_code]), :], "uf")
        plot_race_chart(
            uf_df,
            f"Accumulated rainfall by states of {get_region_name(region_code)} region of Brazil",
            500,
            sort="desc",
        )


def race_plot(df, region_code):
    rainfall_df = set_accumulated_rainfall(df)
    plot_rainfall_byregion(rainfall_df)
    plot_rainfall_bystate(rainfall_df, region_code)


sample_size = display_header()
stations_location()
weather_df = get_sample(sample_size)

"""plot_corretation(weather_df)

df_by_region = set_weather_by_region(weather_df)
plot_brazil_max_temp(df_by_region)
plot_brazil_regions_max_temp(df_by_region)

plot_variables_byregion(weather_df)

humidity_df = set_air_humidity_byregion(weather_df)
plot_air_humidity_byregion(humidity_df)
plot_air_humidity_selected_region(humidity_df, "S")"""

race_plot(weather_df, "SE")
