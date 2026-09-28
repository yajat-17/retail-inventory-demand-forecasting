# ============================================================
# RETAIL INVENTORY DEMAND FORECASTING & STOCK-OUT PREDICTION
# STREAMLIT DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Inventory Analytics",
    page_icon="📦",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f7f9fc;
    }

    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }

    .risk-high {
        color: #d62728;
        font-weight: bold;
    }

    .risk-low {
        color: #2ca02c;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.title("📦 Retail Inventory Analytics Dashboard")

st.markdown(
    """
    **Retail Inventory Demand Forecasting and Stock-Out Prediction**

    This dashboard provides demand analysis, inventory monitoring,
    stock-out risk detection and inventory reorder recommendations.
    """
)

st.divider()


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    inventory = pd.read_csv(
        "inventory_optimization_results.csv"
    )

    latest = pd.read_csv(
        "latest_inventory_recommendations.csv"
    )

    return inventory, latest


try:

    inventory_df, latest_df = load_data()

except FileNotFoundError:

    st.error(
        "CSV files not found. Make sure these files are in the same "
        "folder as app.py:"
    )

    st.code(
        """
inventory_optimization_results.csv
latest_inventory_recommendations.csv
        """
    )

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

inventory_df["Date"] = pd.to_datetime(
    inventory_df["Date"]
)

latest_df["Date"] = pd.to_datetime(
    latest_df["Date"]
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")


# Store filter

stores = sorted(
    latest_df["Store ID"].unique()
)

selected_store = st.sidebar.selectbox(
    "Select Store",
    ["All"] + stores
)


# Category filter

categories = sorted(
    latest_df["Category"].unique()
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + categories
)


# Region filter

regions = sorted(
    latest_df["Region"].unique()
)

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + regions
)


# Apply filters

filtered_df = latest_df.copy()


if selected_store != "All":

    filtered_df = filtered_df[
        filtered_df["Store ID"] == selected_store
    ]


if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]


if selected_region != "All":

    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]


# ============================================================
# KPI SECTION
# ============================================================

st.header("📊 Executive Overview")


total_products = len(filtered_df)

total_inventory = int(
    filtered_df["Inventory Level"].sum()
)

reorder_products = int(
    (filtered_df["Suggested_Order"] > 0).sum()
)

high_risk_products = int(
    (
        filtered_df["Stockout_Risk"]
        == "High Risk"
    ).sum()
)

urgent_reorders = int(
    (
        filtered_df["Recommendation"]
        == "Urgent Reorder"
    ).sum()
)


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Products",
        total_products
    )


with col2:

    st.metric(
        "Total Inventory",
        f"{total_inventory:,}"
    )


with col3:

    st.metric(
        "Reorder Required",
        reorder_products
    )


with col4:

    st.metric(
        "High Stock-Out Risk",
        high_risk_products
    )


with col5:

    st.metric(
        "Urgent Reorder",
        urgent_reorders
    )


st.divider()


# ============================================================
# INVENTORY STATUS
# ============================================================

st.header("📦 Inventory Status")


status_counts = (
    filtered_df[
        "Inventory_Status"
    ]
    .value_counts()
    .reset_index()
)

status_counts.columns = [
    "Status",
    "Count"
]


fig_status = px.pie(
    status_counts,
    names="Status",
    values="Count",
    title="Inventory Status Distribution"
)

st.plotly_chart(
    fig_status,
    use_container_width=True
)


# ============================================================
# STOCK-OUT RISK
# ============================================================

st.header("🚨 Stock-Out Risk Analysis")


risk_counts = (
    filtered_df[
        "Stockout_Risk"
    ]
    .value_counts()
    .reset_index()
)

risk_counts.columns = [
    "Risk",
    "Count"
]


fig_risk = px.bar(
    risk_counts,
    x="Risk",
    y="Count",
    title="Stock-Out Risk Distribution",
    text="Count"
)

fig_risk.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# ============================================================
# STOCK-OUT PROBABILITY
# ============================================================

st.subheader(
    "Stock-Out Probability by Product"
)


risk_chart_df = (
    filtered_df
    .sort_values(
        "Stockout_Probability",
        ascending=False
    )
    .head(15)
)


fig_probability = px.bar(
    risk_chart_df,
    x="Product ID",
    y="Stockout_Probability",
    color="Stockout_Risk",
    title="Top 15 Products by Stock-Out Probability",
    text="Stockout_Probability"
)

fig_probability.update_traces(
    texttemplate="%{text:.1%}",
    textposition="outside"
)

fig_probability.update_yaxes(
    tickformat=".0%"
)

st.plotly_chart(
    fig_probability,
    use_container_width=True
)


# ============================================================
# DEMAND ANALYSIS
# ============================================================

st.header("📈 Demand Analysis")


category_demand = (
    filtered_df
    .groupby("Category")[
        "Recent_Demand"
    ]
    .mean()
    .reset_index()
)


fig_category_demand = px.bar(
    category_demand,
    x="Category",
    y="Recent_Demand",
    title="Average Recent Demand by Category",
    text="Recent_Demand"
)

fig_category_demand.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

st.plotly_chart(
    fig_category_demand,
    use_container_width=True
)


# ============================================================
# INVENTORY VS DEMAND
# ============================================================

st.subheader(
    "Current Inventory vs Recent Demand"
)


fig_inventory_demand = px.scatter(
    filtered_df,
    x="Recent_Demand",
    y="Inventory Level",
    size="Suggested_Order",
    color="Stockout_Risk",
    hover_data=[
        "Store ID",
        "Product ID",
        "Category",
        "Suggested_Order"
    ],
    title="Inventory Level vs Recent Demand"
)

st.plotly_chart(
    fig_inventory_demand,
    use_container_width=True
)


# ============================================================
# REORDER ANALYSIS
# ============================================================

st.header("🔄 Inventory Reorder Analysis")


reorder_df = filtered_df[
    filtered_df["Suggested_Order"] > 0
].copy()


if len(reorder_df) > 0:

    reorder_category = (
        reorder_df
        .groupby("Category")[
            "Suggested_Order"
        ]
        .sum()
        .reset_index()
    )

    fig_reorder = px.bar(
        reorder_category,
        x="Category",
        y="Suggested_Order",
        title="Suggested Reorder Quantity by Category",
        text="Suggested_Order"
    )

    fig_reorder.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig_reorder,
        use_container_width=True
    )

else:

    st.success(
        "No products currently require reordering "
        "for the selected filters."
    )


# ============================================================
# TOP REORDER PRODUCTS
# ============================================================

st.header("📋 Top Products Requiring Reorder")


top_reorders = (
    filtered_df[
        filtered_df["Suggested_Order"] > 0
    ]
    .sort_values(
        "Suggested_Order",
        ascending=False
    )
    .head(10)
)


if len(top_reorders) > 0:

    display_reorders = top_reorders[
        [
            "Store ID",
            "Product ID",
            "Category",
            "Inventory Level",
            "Recent_Demand",
            "Reorder_Point",
            "Suggested_Order",
            "Stockout_Probability",
            "Stockout_Risk",
            "Recommendation"
        ]
    ].copy()

    display_reorders[
        "Stockout_Probability"
    ] = (
        display_reorders[
            "Stockout_Probability"
        ] * 100
    ).round(2)

    display_reorders = (
        display_reorders.rename(
            columns={
                "Stockout_Probability":
                "Stock-Out Probability (%)"
            }
        )
    )

    st.dataframe(
        display_reorders,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No reorder recommendations "
        "for the selected filters."
    )


# ============================================================
# HIGH-RISK PRODUCTS
# ============================================================

st.header("🚨 High Stock-Out Risk Products")


high_risk_df = filtered_df[
    filtered_df["Stockout_Risk"]
    == "High Risk"
].copy()


if len(high_risk_df) > 0:

    high_risk_display = high_risk_df[
        [
            "Store ID",
            "Product ID",
            "Category",
            "Inventory Level",
            "Recent_Demand",
            "Reorder_Point",
            "Suggested_Order",
            "Stockout_Probability",
            "Recommendation"
        ]
    ].copy()

    high_risk_display[
        "Stockout_Probability"
    ] = (
        high_risk_display[
            "Stockout_Probability"
        ] * 100
    ).round(2)

    high_risk_display = (
        high_risk_display.rename(
            columns={
                "Stockout_Probability":
                "Stock-Out Probability (%)"
            }
        )
    )

    st.dataframe(
        high_risk_display,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No high stock-out risk products "
        "for the selected filters."
    )


# ============================================================
# INVENTORY TABLE
# ============================================================

st.header("📋 Complete Inventory Recommendations")


complete_table = filtered_df[
    [
        "Store ID",
        "Product ID",
        "Category",
        "Region",
        "Inventory Level",
        "Recent_Demand",
        "Safety_Stock",
        "Reorder_Point",
        "Suggested_Order",
        "Stockout_Probability",
        "Stockout_Risk",
        "Inventory_Status",
        "Recommendation"
    ]
].copy()


complete_table[
    "Stockout_Probability"
] = (
    complete_table[
        "Stockout_Probability"
    ] * 100
).round(2)


complete_table = (
    complete_table.rename(
        columns={
            "Stockout_Probability":
            "Stock-Out Probability (%)"
        }
    )
)


st.dataframe(
    complete_table,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD DATA
# ============================================================

st.header("⬇️ Download Results")


csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="📥 Download Inventory Recommendations",
    data=csv_data,
    file_name="inventory_recommendations.csv",
    mime="text/csv"
)


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.divider()

st.header("ℹ️ About the Project")

st.markdown(
    """
    ### Retail Inventory Demand Forecasting and Stock-Out Prediction

    This project combines machine learning and inventory analytics
    to help retailers make better inventory decisions.

    **Main components:**

    - Demand Forecasting
    - Stock-Out Prediction
    - Inventory Optimization
    - Reorder Point Calculation
    - Safety Stock Calculation
    - Suggested Order Quantity
    - Interactive Data Visualization

    **Machine Learning Models:**

    - Random Forest Regressor for Demand Forecasting
    - Random Forest Classifier for Stock-Out Prediction

    **Inventory Optimization:**

    - Recent Demand
    - Demand Variability
    - Safety Stock
    - Reorder Point
    - Stock-Out Probability
    - Suggested Reorder Quantity
    """
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Retail Inventory Analytics | B.Sc. Data Science Project"
)