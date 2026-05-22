import plotly.express as px
import pandas as pd

def revenue_trend(df):

    revenue_by_day = (
        df.groupby(
            df["Order Date and Time"].dt.date
        )["order_value"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        revenue_by_day,
        x="Order Date and Time",
        y="order_value",
        title="Revenue Trend"
    )

    return fig

def delivery_time_histogram(df):

    fig2 = px.histogram(
        df,
        x="delivery_time_min",
        nbins=20,
        title="Delivery Time Distribution"
    )

    return fig2


def top_restaurants(df):

    restaurant_orders = (
        df["restaurant_id"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    restaurant_orders.columns = [
        "Restaurant",
        "Orders"
    ]

    fig = px.bar(
        restaurant_orders,
        x="Restaurant",
        y="Orders",
        title="Top Restaurants by Orders"
    )

    return fig

def financial_breakdown(df):

    financials = {
        "Revenue": df["order_value"].sum(),
        "Delivery Fees": df["delivery_fee"].sum(),
        "Commission Fees": df["Commission Fee"].sum(),
        "Refunds": df["Refunds/Chargebacks"].sum()
    }

    financial_df = pd.DataFrame({
        "Category": financials.keys(),
        "Amount": financials.values()
    })

    fig = px.bar(
        financial_df,
        x="Category",
        y="Amount",
        title="Financial Breakdown",
        template="plotly_dark"
    )

    return fig

def payment_revenue(df):

    payment_df = (
        df.groupby("payment_method")["order_value"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        payment_df,
        x="payment_method",
        y="order_value",
        title="Revenue by Payment Method"
    )

    return fig
def peak_hours(df):

    hourly_orders = (
        df.groupby("order_hour")
        .size()
        .reset_index(name="orders")
    )

    fig = px.line(
        hourly_orders,
        x="order_hour",
        y="orders",
        title="Peak Order Hours"
    )

    return fig