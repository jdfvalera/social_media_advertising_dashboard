import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="Marketing Campaign Dashboard",
    layout="wide"
)

# DATA LOADING
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])

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
    [df["Date"].max(), df["Date"].max()]
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

goal = st.sidebar.multiselect(
    "Campaign Goal",
    sorted(df["Campaign_Goal"].unique()),
    default=list(df["Campaign_Goal"].unique())
)

audience = st.sidebar.multiselect(
    "Target Audience",
    sorted(df["Target_Audience"].unique()),
    default=list(df["Target_Audience"].unique())
)

filtered_df = df[
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1])) &
    (df["Company"].isin(company)) &
    (df["Channel_Used"].isin(channel)) &
    (df["Campaign_Goal"].isin(goal)) &
    (df["Target_Audience"].isin(audience))
]

# PAGE NAVIGATION
page = st.sidebar.radio(
    "Page",
    [
        "Executive Overview",
        "Audience & Engagement",
        "Efficiency & Risk",
        "Campaign Deep Dive"
    ]
)

# EXECUTIVE OVERVIEW
if page == "Executive Overview":
    st.title("Executive Overview")

    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric("Total Spend", f"${filtered_df['Acquisition_Cost'].sum():,.0f}")
    k2.metric("Impressions", f"{filtered_df['Impressions'].sum():,.0f}")
    k3.metric("Clicks", f"{filtered_df['Clicks'].sum():,.0f}")
    k4.metric("Avg ROI", f"{filtered_df['ROI'].mean():.2f}")
    k5.metric("Cost / Conversion", f"${filtered_df['Cost_per_Conversion'].mean():.2f}")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            filtered_df.groupby("Channel_Used", as_index=False)["ROI"].mean()
                .sort_values("ROI", ascending=False),
            x="ROI",
            y="Channel_Used",
            orientation="h",
            title="Which Channels Actually Perform"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            filtered_df,
            x="Clicks",
            y="ROI",
            size="Impressions",
            color="Channel_Used",
            title="Scale vs Efficiency"
        )
        st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        filtered_df.groupby("Campaign_Goal", as_index=False)["Clicks"].sum(),
        x="Campaign_Goal",
        y="Clicks",
        title="Where Volume Is Coming From"
    )
    st.plotly_chart(fig, use_container_width=True)

# AUDIENCE & ENGAGEMENT
elif page == "Audience & Engagement":
    st.title("Audience & Engagement")


    fig = px.scatter(
        filtered_df,
        x="Engagement_Score",
        y="Conversion_Rate",
        size="Clicks",
        color="Target_Audience",
        title="Engagement vs Conversion"
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            filtered_df.groupby("Customer_Segment", as_index=False)["Conversion_Rate"].mean(),
            x="Customer_Segment",
            y="Conversion_Rate",
            title="Conversion by Segment"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            filtered_df.groupby("Language", as_index=False)["CTR"].mean(),
            x="Language",
            y="CTR",
            title="CTR by Language"
        )
        st.plotly_chart(fig, use_container_width=True)

# EFFICIENCY & RISK
elif page == "Efficiency & Risk":
    st.title("Efficiency & Risk")


    worst = (
        filtered_df.groupby("Campaign_ID", as_index=False)
        .agg({
            "ROI": "mean",
            "Acquisition_Cost": "sum"
        })
        .sort_values("ROI")
        .head(10)
    )

    fig = px.bar(
        worst,
        x="ROI",
        y="Campaign_ID",
        orientation="h",
        title="Lowest ROI Campaigns"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(
        filtered_df,
        x="Duration",
        y="Cost_per_Conversion",
        color="Campaign_Goal",
        title="Campaign Duration vs Cost Efficiency"
    )
    st.plotly_chart(fig, use_container_width=True)

# CAMPAIGN DEEP DIVE
elif page == "Campaign Deep Dive":
    st.title("Campaign Deep Dive")


    display_df = (
        filtered_df[
            [
                "Campaign_ID",
                "Company",
                "Channel_Used",
                "Campaign_Goal",
                "Target_Audience",
                "Customer_Segment",
                "Language",
                "Location",
                "Duration",
                "Impressions",
                "Clicks",
                "CTR",
                "ROI",
                "Estimated_Conversions",
                "Cost_per_Conversion"
            ]
        ]
        .sort_values("ROI", ascending=False)
    )

    st.markdown(f"**Showing {len(display_df):,} campaigns** (scroll to view all)")

    st.download_button(
        label="Download filtered data as CSV",
        data=display_df.to_csv(index=False),
        file_name="campaign_deep_dive.csv",
        mime="text/csv"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        height=600
    )
