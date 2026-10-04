def predict_demand(model, df):
    features = ['Price', 'Discount_Percent', 'Current_Stock',
                    'Supplier_Lead_Time_Days', 'Day_of_Week',
                    'Month', 'Is_Weekend', 'Sales_Lag_1',
                    'Sales_Lag_7', 'Sales_Rolling_7_Days']
    x = df[features]
    predictions = model.predict(x)
    return predictions

def calculate_predicted_stockout(df):

    df["Predicted_Demand"] = df["Predicted_Demand"].clip(lower=0.1)

    df["Predicted_Days_To_Stockout"] = (
        df["Current_Stock"] / df["Predicted_Demand"]
    )

    return df

def get_latest_predictions(df):

    latest = (
        df.sort_values("Date")
          .groupby("Product_Name")
          .tail(1)
          .copy()
    )
    latest["Reorder_Required"] = (
        latest["Predicted_Days_To_Stockout"] <= latest["Supplier_Lead_Time_Days"]
    )
    return latest