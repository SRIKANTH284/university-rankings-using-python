import pandas as pd
import plotly.express as px
import streamlit as st

# Emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="University Rankings", page_icon=":mortar_board:", layout="wide")

# ---- READ DATA ----
@st.cache
def get_university_data():
    # Replace the following path with the path to your university ranking data (Excel file)
    data_path = "universityrankings.xlsx"
    df = pd.read_excel(data_path)
    return df

df = get_university_data()

# Convert 'year' column to numeric data type (integer)
df["year"] = df["year"].astype(int)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
country = st.sidebar.multiselect(
    "Select Country:",
    options=df["country"].unique(),
    default=df["country"].unique()
)

year = st.sidebar.slider(
    "Select Year:",
    min_value=df["year"].min(),
    max_value=df["year"].max(),
    value=df["year"].max(),
)

df_selection = df.query("country == @country & year == @year")

# ---- MAIN PAGE ----
st.title(":mortar_board: University Rankings")
st.markdown("##")

# TOP KPI's
top_10_universities = df_selection.nsmallest(10, "world_rank")
st.subheader("Top 10 Universities:")
st.dataframe(top_10_universities)

st.markdown("""---""")

# UNIVERSITY DISTRIBUTION BY COUNTRY [BAR CHART]
university_distribution = df_selection["country"].value_counts().reset_index()
university_distribution.columns = ["Country", "Number of Universities"]

fig_university_distribution = px.bar(
    university_distribution,
    x="Number of Universities",
    y="Country",
    orientation="h",
    title="<b>University Distribution by Country</b>",
    color_discrete_sequence=["#0083B8"] * len(university_distribution),
    template="plotly_white",
)
fig_university_distribution.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),
)

st.plotly_chart(fig_university_distribution, use_container_width=True)

# UNIVERSITY RANKING TREND [LINE CHART]
fig_ranking_trend = px.line(
    df_selection,
    x="year",
    y="world_rank",
    color="institution",
    title="<b>University Ranking Trend</b>",
    template="plotly_white",
)
fig_ranking_trend.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
)

st.plotly_chart(fig_ranking_trend, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
