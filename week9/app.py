
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="World Happiness Dashboard", layout="wide")

st.title("🌍 World Happiness Dashboard")
st.caption("Explore happiness scores and compare countries around the world.")

df = pd.read_csv("data/world_happiness_2023.csv")

df = df.rename(columns={
    "Country name": "Country",
    "Regional indicator": "Region",
    "Ladder score": "Score",
    "Logged GDP per capita": "GDP",
    "Social support": "Social_Support",
    "Healthy life expectancy": "Life_Expectancy",
    "Freedom to make life choices": "Freedom",
    "Generosity": "Generosity",
    "Perceptions of corruption": "Corruption"
})

st.sidebar.header("Dashboard Filters")

regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

top_n = st.sidebar.slider("Number of countries", 5, 30, 10)

filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]

if filtered_df.empty:
    st.warning("No countries found for this selection.")
    st.stop()

global_average = df["Score"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Countries", len(filtered_df))
col2.metric("Average Happiness Score", round(filtered_df["Score"].mean(), 2))

happiest_country = filtered_df.loc[filtered_df["Score"].idxmax(), "Country"]
col3.metric("Happiest Country", happiest_country)

st.subheader("Top Happiest Countries")

top_countries = filtered_df.nlargest(top_n, "Score")

fig1 = px.bar(
    top_countries.sort_values("Score"),
    x="Score",
    y="Country",
    orientation="h",
    color="Score",
    color_continuous_scale="Viridis",
    title="Happiness Scores by Country"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("Countries Above and Below the Global Average")

comparison_df = filtered_df.copy()
comparison_df["Difference"] = comparison_df["Score"] - global_average

max_difference = comparison_df["Difference"].abs().max()

fig2 = px.bar(
    comparison_df.sort_values("Difference"),
    x="Difference",
    y="Country",
    orientation="h",
    color="Difference",
    color_continuous_scale="RdBu",
    color_continuous_midpoint=0,
    range_color=[-max_difference, max_difference],
    title="Difference from Global Average Happiness Score"
)

fig2.add_vline(
    x=0,
    line_dash="dash",
    line_color="black",
    annotation_text=f"Global Average: {global_average:.2f}",
    annotation_position="top"
)

fig2.update_layout(
    xaxis_title="Difference from Global Average",
    yaxis_title="Country"
)

st.plotly_chart(fig2, use_container_width=True)

st.caption("Source: World Happiness Report 2023")
