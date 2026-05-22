import pandas as pd

def load_data():

    df = pd.read_csv("food_delivery_clean.csv")

    # DATETIME
    df["Order Date and Time"] = pd.to_datetime(
        df["Order Date and Time"]
    )

    df["Delivery Date and Time"] = pd.to_datetime(
        df["Delivery Date and Time"]
    )

    # RENAME
    df = df.rename(columns={
        "Order Value": "order_value",
        "Delivery Fee": "delivery_fee",
        "Payment Method": "payment_method",
        "Restaurant ID": "restaurant_id"
    })

    # DELIVERY TIME
    df["delivery_time_min"] = (
        df["Delivery Date and Time"]
        - df["Order Date and Time"]
    ).dt.total_seconds() / 60

    df["order_hour"] = df["Order Date and Time"].dt.hour

    return df
