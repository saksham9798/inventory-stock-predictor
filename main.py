from data_preproces import load_data
from feature import create_features
from train_model import train_model
from prediction import predict_demand
from prediction import calculate_predicted_stockout
from prediction import get_latest_predictions
from invnt_anls import calculate_inventory_analysis
from visualization import plot_stockout_risk


df = load_data()

df = create_features(df)

model = train_model(df)

predictions = predict_demand(model, df)
df["Predicted_Demand"] = predictions

df = calculate_predicted_stockout(df)

# Get latest record for every product
latest = get_latest_predictions(df)

print("\nFINAL PREDICTION:")
print(latest[[ 
    "Product_Name", "Current_Stock", "Predicted_Demand", 
    "Predicted_Days_To_Stockout", "Supplier_Lead_Time_Days", "Reorder_Required"]]
)
product_data = calculate_inventory_analysis(df)


plot_stockout_risk(product_data)