def create_features(df):

    df["Day_of_Week"] = df["Date"].dt.dayofweek

    df["Month"] = df["Date"].dt.month

    df["Is_Weekend"] = (
        df["Day_of_Week"] >= 5
    ).astype(int)

    #Previous Sales
    df["Sales_Lag_1"] = (
        df.groupby("Product_Name")["Units_Sold"].shift(1)
    )
    df["Sales_Lag_7"] = (
        df.groupby("Product_Name")["Units_Sold"].shift(7)
    )

    #Recent demand
    df["Sales_Rolling_7_Days"] = (
        df.groupby("Product_Name")["Units_Sold"].transform(
            lambda x: x.shift(1).rolling(7).mean()
        )
    )

    df["Next_Day_Sales"] = (
        df.groupby("Product_Name")["Units_Sold"].shift(-1)
    )
    
    df = df.dropna()

    return df