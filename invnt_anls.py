import numpy as np

def calculate_inventory_analysis(df):

    avg_sales = df.groupby('Product_Name')["Units_Sold"].mean()
    print("average daily sales: \n",np.round(avg_sales, 2))
    product_data = df.groupby('Product_Name').agg({
        "Current_Stock": "last",
        "Units_Sold": "mean",
        "Supplier_Lead_Time_Days": "first"
    })
    product_data['Days_To_Stockout'] = (
        product_data['Current_Stock'] /product_data['Units_Sold']
    )
    product_data['Risk'] = (
    product_data['Days_To_Stockout'].apply(risk_level)
    )
    print(
        "days to stock out:\n",
        product_data.round(2)
    )
    return product_data

def risk_level(days):

    if days <= 5:
        return "Critical"

    elif days <= 10:
        return "High"

    elif days <= 14:
        return "Medium"

    else:
        return "Low"

def analyze_predicted_stockout(df):

    df = df.copy()

    df["Predicted_Demand"] = (
        df["Predicted_Demand"].clip(lower=0.1)
    )

    df["Predicted_Days_To_Stockout"] = (
        df["Current_Stock"] / df["Predicted_Demand"]
    )

    df["Reorder_Required"] = (
        df["Predicted_Days_To_Stockout"] <= df["Supplier_Lead_Time_Days"]
    )

    return df