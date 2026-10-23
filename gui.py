
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
import calendar

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from data_preproces import load_data
from feature import create_features
from train_model import train_model
from prediction import predict_demand


# ---------------- COLORS ----------------

BG = "#F4F7FB"
WHITE = "#FFFFFF"
NAVY = "#172554"
BLUE = "#2563EB"
TEXT = "#1E293B"
MUTED = "#64748B"
GREEN = "#15803D"
RED = "#DC2626"
BORDER = "#E2E8F0"


# ---------------- LOAD PROJECT DATA ----------------

df = load_data()
df = create_features(df)

model = train_model(df)

df["Predicted_Demand"] = predict_demand(model, df)
df["Predicted_Demand"] = df["Predicted_Demand"].clip(lower=0)

df["Year"] = df["Date"].dt.year

products = sorted(df["Product_Name"].unique())
years = sorted(df["Year"].unique())
months = list(calendar.month_name)[1:]


# ---------------- WINDOW ----------------

root = tk.Tk()
root.title("StockWise | Inventory Predictor")
root.geometry("1300x865")
root.minsize(1200, 865)
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Modern.TCombobox",
    padding=8,
    fieldbackground=WHITE,
    background=WHITE,
    foreground=TEXT
)

style.configure(
    "Modern.TEntry",
    padding=9,
    fieldbackground=WHITE,
    foreground=TEXT
)

style.configure(
    "Modern.TButton",
    padding=(14, 10),
    font=("Segoe UI", 10, "bold")
)

style.map(
    "Modern.TButton",
    background=[("active", "#1D4ED8")],
    foreground=[("active", WHITE)]
)


# ---------------- HELPER FUNCTIONS ----------------

def make_card(parent, title, value, subtitle=""):
    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    tk.Label(
        card,
        text=title.upper(),
        bg=WHITE,
        fg=MUTED,
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="w", padx=18, pady=(16, 7))

    value_label = tk.Label(
        card,
        text=value,
        bg=WHITE,
        fg=TEXT,
        font=("Segoe UI", 23, "bold")
    )
    value_label.pack(anchor="w", padx=18)

    subtitle_label = tk.Label(
        card,
        text=subtitle,
        bg=WHITE,
        fg=MUTED,
        font=("Segoe UI", 9)
    )
    subtitle_label.pack(anchor="w", padx=18, pady=(5, 16))

    return card, value_label, subtitle_label


def add_section(parent, title, subtitle=None):
    tk.Label(
        parent,
        text=title,
        bg=WHITE,
        fg=TEXT,
        font=("Segoe UI", 13, "bold")
    ).pack(anchor="w", padx=18, pady=(16, 2))

    if subtitle:
        tk.Label(
            parent,
            text=subtitle,
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=18, pady=(0, 10))


# ---------------- SIDEBAR ----------------

sidebar = tk.Frame(root, bg=NAVY, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="◈  StockWise",
    bg=NAVY,
    fg=WHITE,
    font=("Segoe UI", 19, "bold")
).pack(anchor="w", padx=22, pady=(30, 5))

tk.Label(
    sidebar,
    text="INVENTORY INTELLIGENCE",
    bg=NAVY,
    fg="#93C5FD",
    font=("Segoe UI", 8, "bold")
).pack(anchor="w", padx=23, pady=(0, 35))

tk.Label(
    sidebar,
    text="  ▦   Overview",
    bg="#263B70",
    fg=WHITE,
    font=("Segoe UI", 11, "bold"),
    padx=12,
    pady=12
).pack(fill="x", padx=12)

tk.Label(
    sidebar,
    text="  ◷   Demand Analytics",
    bg=NAVY,
    fg="#CBD5E1",
    font=("Segoe UI", 10),
    padx=12,
    pady=14
).pack(fill="x", padx=12)

tk.Label(
    sidebar,
    text="  ▣   Stock Calculator",
    bg=NAVY,
    fg="#CBD5E1",
    font=("Segoe UI", 10),
    padx=12,
    pady=10
).pack(fill="x", padx=12)

tk.Label(
    sidebar,
    text="Inventory Stock-Out Predictor\nDeveloped by: Saksham Singh\n© 2026 StockWise Inc.",
    bg=NAVY,
    fg="#CBD5E1",
    justify="left",
    font=("Segoe UI", 9),
    wraplength=175
).pack(side="bottom", anchor="w", padx=22, pady=25)


# ---------------- MAIN WORKSPACE ----------------

workspace = tk.Frame(root, bg=BG)
workspace.pack(side="left", fill="both", expand=True)

header = tk.Frame(workspace, bg=WHITE, height=90)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="Inventory Dashboard",
    bg=WHITE,
    fg=TEXT,
    font=("Segoe UI", 22, "bold")
).pack(anchor="w", padx=26, pady=(16, 0))

tk.Label(
    header,
    text="Monitor demand, estimate stock-out dates, and plan reorders.",
    bg=WHITE,
    fg=MUTED,
    font=("Segoe UI", 10)
).pack(anchor="w", padx=27, pady=(2, 12))


# Content area
content = tk.Frame(workspace, bg=BG)
content.pack(fill="both", expand=True, padx=24, pady=18)


# ---------------- FILTERS ----------------

filters = tk.Frame(content, bg=WHITE,
                   highlightbackground=BORDER,
                   highlightthickness=1)
filters.pack(fill="x")

add_section(
    filters,
    "Product analysis",
    "Choose a product and reporting period."
)

filter_row = tk.Frame(filters, bg=WHITE)
filter_row.pack(fill="x", padx=18, pady=(0, 18))

tk.Label(
    filter_row, text="PRODUCT",
    bg=WHITE, fg=MUTED,
    font=("Segoe UI", 9, "bold")
).grid(row=0, column=0, sticky="w", padx=(0, 8))

tk.Label(
    filter_row, text="MONTH",
    bg=WHITE, fg=MUTED,
    font=("Segoe UI", 9, "bold")
).grid(row=0, column=1, sticky="w", padx=(0, 8))

tk.Label(
    filter_row, text="YEAR",
    bg=WHITE, fg=MUTED,
    font=("Segoe UI", 9, "bold")
).grid(row=0, column=2, sticky="w", padx=(0, 8))

product_var = tk.StringVar(value=products[0])
month_var = tk.StringVar(value=months[0])
year_var = tk.StringVar(value=str(years[-1]))

product_box = ttk.Combobox(
    filter_row, textvariable=product_var,
    values=products, state="readonly",
    style="Modern.TCombobox", width=23
)
product_box.grid(row=1, column=0, sticky="ew", padx=(0, 18))

month_box = ttk.Combobox(
    filter_row, textvariable=month_var,
    values=months, state="readonly",
    style="Modern.TCombobox", width=15
)
month_box.grid(row=1, column=1, sticky="ew", padx=(0, 18))

year_box = ttk.Combobox(
    filter_row, textvariable=year_var,
    values=[str(y) for y in years],
    state="readonly",
    style="Modern.TCombobox", width=10
)
year_box.grid(row=1, column=2, sticky="ew", padx=(0, 18))

filter_row.columnconfigure(0, weight=2)
filter_row.columnconfigure(1, weight=1)
filter_row.columnconfigure(2, weight=1)


# ---------------- SUMMARY CARDS ----------------

cards = tk.Frame(content, bg=BG)
cards.pack(fill="x", pady=16)

card1, demand_value, demand_note = make_card(
    cards, "Actual daily demand", "--", "Historical monthly average"
)
card2, predicted_value, predicted_note = make_card(
    cards, "Predicted daily demand", "--", "Model estimate"
)
card3, stock_value, stock_note = make_card(
    cards, "Recorded stock", "--", "Latest stock in selected month"
)
card4, stockout_value, stockout_note = make_card(
    cards, "Estimated stock life", "--", "Based on predicted demand"
)

for card in (card1, card2, card3, card4):
    card.pack(side="left", fill="both", expand=True, padx=(0, 10))


# ---------------- CHART AND CALCULATOR ----------------

lower = tk.Frame(content, bg=BG)
lower.pack(fill="both", expand=True)

chart_panel = tk.Frame(
    lower, bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)
chart_panel.pack(side="left", fill="both", expand=True, padx=(0, 12))

add_section(
    chart_panel,
    "Demand trend",
    "Daily actual demand versus predicted demand"
)

figure = Figure(figsize=(6, 3.1), dpi=100)
ax = figure.add_subplot(111)
figure.subplots_adjust(left=0.12, right=0.96, top=0.92, bottom=0.18)

chart = FigureCanvasTkAgg(figure, master=chart_panel)
chart.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 12))


calculator = tk.Frame(
    lower, bg=WHITE, width=285,
    highlightbackground=BORDER,
    highlightthickness=1
)
calculator.pack(side="right", fill="y")
calculator.pack_propagate(False)

add_section(
    calculator,
    "Stock calculator",
    "Test a different available quantity."
)

tk.Label(
    calculator,
    text="MANUAL STOCK QUANTITY",
    bg=WHITE, fg=MUTED,
    font=("Segoe UI", 9, "bold")
).pack(anchor="w", padx=18, pady=(1, 6))

stock_entry = ttk.Entry(
    calculator, style="Modern.TEntry"
)
stock_entry.pack(fill="x", padx=18)
stock_entry.insert(0, "100")



tk.Label(
    calculator,
    text="Enter the quantity currently available.",
    bg=WHITE, fg=MUTED,
    font=("Segoe UI", 8),
    wraplength=240
).pack(anchor="w", padx=18, pady=(5, 12))

manual_result = tk.Label(
    calculator,
    text="Enter a stock quantity to estimate how long it will last.",
    bg="#EFF6FF",
    fg=TEXT,
    font=("Segoe UI", 10),
    justify="left",
    wraplength=235,
    padx=12,
    pady=14
)
manual_result.pack(fill="x", padx=18, pady=(0, 12))

current_daily_demand = 0
current_lead_time = 0


# ---------------- ANALYSIS ----------------

def analyze_item():
    global current_daily_demand, current_lead_time

    product = product_var.get()
    month_number = months.index(month_var.get()) + 1
    selected_year = int(year_var.get())

    selected = df[
        (df["Product_Name"] == product) &
        (df["Date"].dt.month == month_number) &
        (df["Date"].dt.year == selected_year)
    ].copy()

    if selected.empty:
        messagebox.showinfo(
            "No data",
            "No records are available for this product and month."
        )
        return

    selected = selected.sort_values("Date")

    actual_avg = selected["Units_Sold"].mean()
    predicted_avg = selected["Predicted_Demand"].mean()
    latest_stock = selected.iloc[-1]["Current_Stock"]
    lead_time = selected["Supplier_Lead_Time_Days"].iloc[-1]

    current_daily_demand = max(float(predicted_avg), 0.1)
    current_lead_time = float(lead_time)

    days_left = max(float(latest_stock), 0) / current_daily_demand

    demand_value.config(text=f"{actual_avg:.1f} units")
    predicted_value.config(text=f"{predicted_avg:.1f} units")
    stock_value.config(text=f"{latest_stock:.0f} units")
    stockout_value.config(text=f"{days_left:.1f} days")

    demand_note.config(text=f"Average for {month_var.get()}")
    predicted_note.config(text="Average model prediction per day")
    stock_note.config(text=f"At {selected['Date'].iloc[-1].strftime('%d %b %Y')}")
    stockout_note.config(text="Estimated using recorded stock")

    # Update actual and predicted demand chart
    ax.clear()
    ax.plot(
        selected["Date"], selected["Units_Sold"],
        label="Actual demand", linewidth=2,
        color="#2563EB"
    )
    ax.plot(
        selected["Date"], selected["Predicted_Demand"],
        label="Predicted demand", linewidth=2,
        color="#F59E0B"
    )

    ax.set_ylabel("Units sold")
    ax.grid(axis="y", alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    figure.autofmt_xdate()
    chart.draw()

    # Refresh manual stock estimate
    calculate_manual_stock()


# ---------------- MANUAL STOCK CALCULATOR ----------------

def calculate_manual_stock():
    try:
        quantity = float(stock_entry.get())

        if quantity < 0:
            raise ValueError

        if current_daily_demand <= 0:
            messagebox.showinfo(
                "Select a product",
                "Analyze a product and month first."
            )
            return

        days = quantity / current_daily_demand
        estimated_date = date.today() + timedelta(days=int(days))

        if days <= current_lead_time:
            status = "REORDER NOW"
            status_color = RED
        elif days <= current_lead_time + 3:
            status = "REORDER SOON"
            status_color = "#B45309"
        else:
            status = "STOCK LOOKS SUFFICIENT"
            status_color = GREEN

        manual_result.config(
            text=(
                f"Estimated stock life\n"
                f"{days:.1f} days\n\n"
                f"Estimated depletion date\n"
                f"{estimated_date.strftime('%d %b %Y')}\n\n"
                f"Supplier lead time: {current_lead_time:.0f} days\n\n"
                f"{status}"
            ),
            fg=status_color
        )

    except ValueError:
        messagebox.showerror(
            "Invalid quantity",
            "Enter a valid non-negative number."
        )


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(filter_row, bg=WHITE)
button_frame.grid(row=1, column=3, sticky="e")

analyze_button = tk.Button(
    button_frame,
    text="Analyze product  →",
    command=analyze_item,
    bg=BLUE, fg=WHITE,
    activebackground="#1D4ED8",
    activeforeground=WHITE,
    relief="flat", bd=0,
    cursor="hand2",
    font=("Segoe UI", 10, "bold"),
    padx=18, pady=11
)
analyze_button.pack()

tk.Button(
    calculator,
    text="Calculate stock life",
    command=calculate_manual_stock,
    bg=BLUE, fg=WHITE,
    activebackground="#1D4ED8",
    activeforeground=WHITE,
    relief="flat", bd=0,
    cursor="hand2",
    font=("Segoe UI", 10, "bold"),
    padx=12, pady=11
).pack(fill="x", padx=18, pady=(0, 18))


# Update the dashboard when the user presses Enter in the stock field
stock_entry.bind("<Return>", lambda event: calculate_manual_stock())

# Show initial analysis
analyze_item()

root.mainloop()
