def total_revenue(df):
    return df["order_value"].sum(), df["order_value"].sum()

def avg_delivery_time(df):
    return df["delivery_time_min"].mean()