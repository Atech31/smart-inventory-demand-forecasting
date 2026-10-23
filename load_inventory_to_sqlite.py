import sqlite3
import pandas as pd

# Load CSV files
df_products = pd.read_csv('products.csv')
df_sales = pd.read_csv('daily_sales.csv')
df_inventory = pd.read_csv('current_inventory.csv')

# Connect to SQLite database
conn = sqlite3.connect('inventory_analytics.db')

# Write dataframes to SQLite tables
df_products.to_sql('products', conn, if_exists='replace', index=False)
df_sales.to_sql('daily_sales', conn, if_exists='replace', index=False)
df_inventory.to_sql('current_inventory', conn, if_exists='replace', index=False)

print("Inventory datasets successfully loaded into inventory_analytics.db!")
conn.close()