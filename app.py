import streamlit as st
import warnings
import pandas as pd

from utils.load_data import load_data
from utils.charts import (
    revenue_trend,
    delivery_time_histogram,
    top_restaurants,
    financial_breakdown,
    payment_revenue
)

warnings.filterwarnings("ignore")

# ======================
# CONFIG
# ======================

st.set_page_config(
    layout="wide",
    page_title="DeliveryOps Intelligence"
)

# ======================
# LOAD DATA
# ======================

df = load_data()

# ======================
# FILTERS (SIDEBAR)
# ======================

st.sidebar.title("Filters")

payment_filter = st.sidebar.selectbox(
    "Payment Method",
    ["All"] + list(df["payment_method"].unique())
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [
        df["Order Date and Time"].min(),
        df["Order Date and Time"].max()
    ]
)

if payment_filter != "All":
    df = df[df["payment_method"] == payment_filter]

start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

df = df[
    (df["Order Date and Time"] >= start_date)
    & (df["Order Date and Time"] <= end_date)
]

# ======================
# METRICS
# ======================

profit = (
    df["order_value"].sum()
    - df["delivery_fee"].sum()
    - df["Refunds/Chargebacks"].sum()
)

refund_rate = (
    df["Refunds/Chargebacks"].sum()
    / df["order_value"].sum()
) * 100

profit_margin = (profit / df["order_value"].sum()) * 100

avg_delivery = df["delivery_time_min"].mean()

# ======================
# TITLE
# ======================

st.title("DeliveryOps Intelligence Dashboard")

# ======================
# ALERTS
# ======================

if refund_rate > 5:
    st.error("Refund rate is above acceptable threshold.")

if avg_delivery > 45:
    st.warning(
        f"Average delivery time is elevated ({avg_delivery:.1f} min)."
    )

# ======================
# KPI ROW
# ======================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Orders", df.shape[0])

with col2:
    st.metric(
        "Revenue",
        f"${df['order_value'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Avg Order Value",
        f"${df['order_value'].mean():.2f}"
    )

with col4:
    st.metric(
        "Avg Delivery Time",
        f"{avg_delivery:.1f} min"
    )

with col5:
    st.metric(
        "Profit",
        f"${profit:,.0f}"
    )

# ======================
# TABS
# ======================

tab1, tab2, tab3 = st.tabs(
    ["Overview", "Operations", "Financial"]
)

# ======================
# OVERVIEW
# ======================

with tab1:

    col_left, col_right = st.columns(2)

    with col_left:
        fig1 = revenue_trend(df)
        st.plotly_chart(fig1, use_container_width=True)

    with col_right:
        fig2 = delivery_time_histogram(df)
        st.plotly_chart(fig2, use_container_width=True)

# ======================
# OPERATIONS
# ======================

with tab2:

    st.subheader("Top Restaurants")

    fig3 = top_restaurants(df)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Payment Behavior")

    fig5 = payment_revenue(df)
    st.plotly_chart(fig5, use_container_width=True)

# ======================
# FINANCIAL
# ======================

with tab3:

    colA, colB = st.columns(2)

    with colA:
        st.metric("Profit Margin", f"{profit_margin:.2f}%")

    with colB:
        st.metric("Refund Rate", f"{refund_rate:.2f}%")

    fig4 = financial_breakdown(df)
    st.plotly_chart(fig4, use_container_width=True)