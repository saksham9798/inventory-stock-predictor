import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def plot_stockout_risk(product_data):

    risk_colors = {
        "Critical": "red",
        "High": "orange",
        "Medium": "yellow",
        "Low": "green"
    }

    colors = product_data["Risk"].map(risk_colors)

    plt.barh(
        product_data.index,
        product_data["Days_To_Stockout"],
        color=colors
    )
    
    plt.xlabel("Estimated Days to Stock Out")
    plt.ylabel("Product")
    plt.title("Inventory Stock Details")

    legend_items = [
        Patch(facecolor="red", label="Critical"),
        Patch(facecolor="orange", label="High"),
        Patch(facecolor="yellow", label="Medium"),
        Patch(facecolor="green", label="Low")
    ]

    plt.legend(handles=legend_items)
    plt.show()