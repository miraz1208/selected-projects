"""
This script is a Streamlit dashboard that can be used to analyze car accidents
in NYC.
The script loads data from a CSV file, filters the data based on user inputs,
and visualizes the data using various charts and maps.

The script imports the following libraries:
- streamlit
- pandas
- numpy
- pydeck
- plotly.express

It defines the following global variable:
- DATA_URL: a string containing the URL of the data file

The script contains the following functions:
- load_data(nrows): loads data from file and
    returns it as a pandas DataFrame.
    The function takes one argument:
- nrows: an integer specifying the maximum number of rows to load from the file

The script contains the following Streamlit elements:
- st.title(): sets the title of the dashboard
- st.markdown(): displays a markdown text
- st.cache_data(): caches the results of a function
    to speed up subsequent executions
- st.header(): displays a header
- st.slider(): displays a slider widget
- st.map(): displays a map
- st.write(): displays various types of data,
    including text, tables, and charts
- st.subheader(): displays a subheader
- st.selectbox(): displays a select box widget
- st.checkbox(): displays a checkbox widget"""

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA_URL = "database.csv"

st.title("Vehicle Collisions in NYC, 2015-Present")
st.markdown(
    "### This application is a Streamlit dashboard that can be used"
    " to analyze car accidents in NYC"
)


@st.cache_data(persist=True)
def load_data(nrows):
    """Loads data from file"""
    data_file = pd.read_csv(
        DATA_URL, nrows=nrows, parse_dates=[["DATE", "TIME"]])
    data_file.dropna(subset=["LATITUDE", "LONGITUDE"], inplace=True)

    def lowercase(var: str):
        return var.lower()

    # lowercase = lambda x: str(x).lower()
    data_file.rename(lowercase, axis="columns", inplace=True)
    data_file.rename(
        columns={"crash_date_crash_time": "date/time"}, inplace=True)
    return data_file


data = load_data(100000)
original_data = data

st.header("Places of injury")
injured_people = st.slider("Number of persons injured", 0, 10)
st.map(
    data.query("`persons injured` >= @injured_people")[
        ["latitude", "longitude"]
    ].dropna(how="any")
)

st.header("How many collisions occur at given time of day?")
hour = st.slider("Hour to look at", 0, 23)
data = data[data["date_time"].dt.hour == hour]

st.markdown(
    "Vehicle collisions between %i:00 and %i:00" % (hour, (hour + 1) % 24))

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))
st.write(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 11,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data[["date_time", "latitude", "longitude"]],
                get_position=["longitude", "latitude"],
                radius=100,
                extruded=True,
                pickable=True,
                elevation_scale=4,
                elevation_range=[0, 1000],
            )
        ],
    )
)

st.subheader(
    "Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (
        data["date_time"].dt.hour >= hour
        ) & (
            data["date_time"].dt.hour < (hour + 1))
]

hist = np.histogram(filtered["date_time"].dt.minute, bins=60, range=(0, 60))[0]

chart_data = pd.DataFrame({"minute": range(60), "crashes": hist})

fig = px.bar(
    chart_data,
    x="minute",
    y="crashes",
    hover_data=["minute", "crashes"],
    height=400
)

st.write(fig)


st.header("Top 5 dangerous streets by affected type")
select = st.selectbox(
    "Affected type of people", ["Pedestrian", "Cyclists", "Motorists"]
)

if select == "Pedestrian":
    st.write(
        original_data.query("`pedestrians injured` >= 1")[
            ["on street name", "pedestrians injured"]
        ]
        .sort_values(
            by=["pedestrians injured"],
            ascending=False,
        )
        .dropna(how="any")[:5]
    )

elif select == "Cyclists":
    st.write(
        original_data.query("`cyclists injured` >= 1")[
            ["on street name", "cyclists injured"]
        ]
        .sort_values(
            by=["cyclists injured"],
            ascending=False,
        )
        .dropna(how="any")[:5]
    )

else:
    st.write(
        original_data.query("`motorists injured` >= 1")[
            ["on street name", "motorists injured"]
        ]
        .sort_values(
            by=["motorists injured"],
            ascending=False,
        )
        .dropna(how="any")[:5]
    )

if st.checkbox("Show Raw Data", False):
    st.subheader("Raw data")
    st.write(data)
