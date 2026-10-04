import pandas as pd
import numpy as np

def load_data():
    df = pd.read_csv('data/inventory_sales.csv')

    print(df.isnull().sum())

    df['Date'] = pd.to_datetime(df['Date'], format= '%d-%m-%Y')

    df = df.sort_values(['Product_Name', 'Date'])

    return df