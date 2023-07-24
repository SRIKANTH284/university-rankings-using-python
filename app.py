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
    df["year"] = df["year"].astype(int)  # Convert 'year' column to integer
    return df

df = get_university_data()

# Function to filter data based on user selection
def filter_data(df, country, year):
    df_selection = df.query("country == @country & year == @year")
    return df_selection

# Function to create university distribution bar chart
def create_university_distribution_chart(df_selection):
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
    
    return fig_university_distribution

# Function to create university ranking trend line chart
def create_ranking_trend_chart(df_selection):
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
    
    return fig_ranking_trend

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
country = st.sidebar.multiselect(
    "Select Country:",
    options=df["country"].unique(),
    default=df["country"].unique()
)

year_min = int(df["year"].min())  # Convert year_min to integer
year_max = int(df["year"].max())  # Convert year_max to integer
year_value = int(df["year"].max())  # Convert year_value to integer

year = st.sidebar.slider(
    "Select Year:",
    min_value=year_min,
    max_value=year_max,
    value=year_value,
)

# Filter data based on user selection
df_selection = filter_data(df, country, year)

# ---- MAIN PAGE ----
st.title(":mortar_board: University Rankings")
st.markdown("##")

# TOP KPI's
top_10_universities = df_selection.nsmallest(10, "world_rank")
st.subheader("Top 10 Universities:")
st.dataframe(top_10_universities)

st.markdown("""---""")

# UNIVERSITY DISTRIBUTION BY COUNTRY [BAR CHART]
fig_university_distribution = create_university_distribution_chart(df_selection)
st.plotly_chart(fig_university_distribution, use_container_width=True)

# UNIVERSITY RANKING TREND [LINE CHART]
fig_ranking_trend = create_ranking_trend_chart(df_selection)
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
