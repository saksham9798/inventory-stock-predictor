from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

def train_model(df):
    features = ['Price', 'Discount_Percent', 'Current_Stock',
                'Supplier_Lead_Time_Days', 'Day_of_Week',
                'Month', 'Is_Weekend', 'Sales_Lag_1',
                'Sales_Lag_7', 'Sales_Rolling_7_Days']
    x = df[features]
    y = df['Next_Day_Sales']

    x_train, x_test, y_train, y_test = train_test_split( 
        x, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100, random_state=42
    )

    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("mean absolute error ",round(mae, 2))
    print("r2 score ", round(r2, 2))

    return model
