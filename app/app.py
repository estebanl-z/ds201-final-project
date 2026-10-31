from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="US Airfare & Passenger Demand", layout="wide")

# Finds the data file no matter which folder you run the app from
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "merged_fare_passengers.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

st.title("US Airfare and Passenger Demand")
st.write("How have airline ticket prices changed, and how are they related to passenger demand?")

# --- Sidebar controls ---
st.sidebar.header("Controls")
year_min, year_max = int(df["year"].min()), int(df["year"].max())
years = st.sidebar.slider("Year range", year_min, year_max, (2015, 2025))
metric = st.sidebar.selectbox("Metric", ["Average fare ($)", "Passengers (millions)"])
show_covid = st.sidebar.checkbox("Highlight COVID-19 period", value=True)

col = {"Average fare ($)": "national_avg_fare",
       "Passengers (millions)": "passengers_millions"}[metric]

d = df[(df["year"] >= years[0]) & (df["year"] <= years[1])].reset_index(drop=True)

# --- Chart 1: trend over time ---
st.subheader(f"{metric} by quarter")
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(d["period"], d[col], linewidth=2)
if show_covid:
    s = d.index[d["period"] == "2020-Q1"]
    e = d.index[d["period"] == "2021-Q2"]
    if len(s) and len(e):
        ax.axvspan(s[0], e[0], color="gray", alpha=0.2)
        ax.text((s[0] + e[0]) / 2, ax.get_ylim()[1] * 0.97, "COVID-19",
                ha="center", va="top")
ax.set_xticks(range(0, len(d), 4))
ax.set_xticklabels(d["period"][::4], rotation=45)
ax.set_ylabel(metric)
st.pyplot(fig)

# --- Chart 2: seasonal pattern ---
st.subheader(f"Median {metric} by quarter (selected years)")
seasonal = d.groupby("quarter")[col].median()
fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.bar(["Q1", "Q2", "Q3", "Q4"], seasonal)
ax2.set_ylabel(metric)
st.pyplot(fig2)