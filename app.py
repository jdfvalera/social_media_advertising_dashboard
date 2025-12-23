import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Marketing Campaign Dashboard",
    layout="wide"
)

# DATA LOADING
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])

    # Clean currency field
    df["Acquisition_Cost"] = (
        df["Acquisition_Cost"]
        .replace(r"[\$,]", "", regex=True)
        .astype(float)
    )

    # Calculated metrics
    df["CTR"] = df["Clicks"] / df["Impressions"]
    df["Estimated_Conversions"] = df["Clicks"] * df["Conversion_Rate"]
    df["CPC"] = df["Acquisition_Cost"] / df["Clicks"]
    df["Cost_per_Conversion"] = df["Acquisition_Cost"] / df["Estimated_Conversions"]

    return df


df = load_data("data/Social_Media_Advertising.csv")

# SIDEBAR FILTERS
st.sidebar.title("Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Date"].min(), df["Date"].max()]
)

company = st.sidebar.multiselect(
    "Company",
    sorted(df["Company"].unique()),
    default=list(df["Company"].unique())
)

channel = st.sidebar.multiselect(
    "Channel",
    sorted(df["Channel_Used"].unique()),
    default=list(df["Channel_Used"].unique())
)

filtered_df = df[
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1])) &
    (df["Company"].isin(company)) &
    (df["Channel_Used"].isin(channel))
]

# PAGE SELECTION
page = st.sidebar.radio(
    "Page",
    [
        "Executive Overview",
        "Channel Performance",
        "Audience Insights",
        "Campaign Deep Dive"
    ]
)

# EXECUTIVE OVERVIEW
if page == "Executive Overview":
    st.title("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Impressions", f"{filtered_df['Impressions'].sum():,.0f}")
    col2.metric("Total Clicks", f"{filtered_df['Clicks'].sum():,.0f}")
    col3.metric("Average ROI", f"{filtered_df['ROI'].mean():.2f}")
    col4.metric("Avg Conversion Rate", f"{filtered_df['Conversion_Rate'].mean():.2%}")

    fig_trend = px.line(
        filtered_df,
        x="Date",
        y=["Clicks", "Impressions"],
        title="Performance Over Time"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    roi_by_channel = (
        filtered_df
        .groupby("Channel_Used", as_index=False)["ROI"]
        .mean()
        .sort_values("ROI", ascending=False)
    )

    fig_roi = px.bar(
        roi_by_channel,
        x="Channel_Used",
        y="ROI",
        title="Average ROI by Channel"
    )
    st.plotly_chart(fig_roi, use_container_width=True)

# CHANNEL PERFORMANCE
elif page == "Channel Performance":
    st.title("Channel Performance")

    channel_table = (
        filtered_df
        .groupby("Channel_Used", as_index=False)
        .agg({
            "Impressions": "sum",
            "Clicks": "sum",
            "CTR": "mean",
            "CPC": "mean",
            "ROI": "mean",
            "Cost_per_Conversion": "mean"
        })
        .sort_values("ROI", ascending=False)
    )

    st.dataframe(channel_table, use_container_width=True)

    fig_ctr = px.bar(
        channel_table,
        x="Channel_Used",
        y="CTR",
        title="CTR by Channel"
    )
    st.plotly_chart(fig_ctr, use_container_width=True)

# AUDIENCE INSIGHTS
elif page == "Audience Insights":
    st.title("Audience Insights")

    fig_audience = px.bar(
        filtered_df.groupby("Target_Audience", as_index=False)["Conversion_Rate"].mean(),
        x="Target_Audience",
        y="Conversion_Rate",
        title="Conversion Rate by Audience"
    )
    st.plotly_chart(fig_audience, use_container_width=True)

    fig_segment = px.bar(
        filtered_df.groupby("Customer_Segment", as_index=False)["Engagement_Score"].mean(),
        x="Customer_Segment",
        y="Engagement_Score",
        title="Engagement by Customer Segment"
    )
    st.plotly_chart(fig_segment, use_container_width=True)

    fig_geo = px.scatter_geo(
        filtered_df,
        locations="Location",
        locationmode="country names",
        size="Clicks",
        title="Geographic Performance"
    )
    st.plotly_chart(fig_geo, use_container_width=True)

# CAMPAIGN DEEP DIVE
elif page == "Campaign Deep Dive":
    st.title("Campaign Deep Dive")

    campaign_table = filtered_df[
        [
            "Campaign_ID",
            "Clicks",
            "Impressions",
            "CTR",
            "ROI",
            "Estimated_Conversions",
            "Cost_per_Conversion"
        ]
    ]

    st.dataframe(campaign_table, use_container_width=True)

    fig_campaign = px.line(
        filtered_df,
        x="Date",
        y="Clicks",
        color="Campaign_ID",
        title="Campaign Click Trends"
    )
    st.plotly_chart(fig_campaign, use_container_width=True)
