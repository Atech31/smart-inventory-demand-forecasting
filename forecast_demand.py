import sqlite3
import pandas as pd
import numpy as np

# Connect to SQLite database
conn = sqlite3.connect('inventory_analytics.db')

# Load daily sales and product info
df_sales = pd.read_sql_query("SELECT * FROM daily_sales", conn)
df_products = pd.read_sql_query("SELECT * FROM products", conn)
conn.close()

# Convert date column to datetime
df_sales['date'] = pd.to_datetime(df_sales['date'])

# Calculate 30-day moving average demand as a baseline forecast
forecast_records = []

for product_id in df_products['product_id']:
    prod_sales = df_sales[df_sales['product_id'] == product_id].sort_values('date')
    
    # Recent 30-day average daily sales
    recent_avg_daily = prod_sales.tail(30)['units_sold'].mean()
    
    # Projected demand for next 30 days
    projected_30_day_demand = int(recent_avg_daily * 30)
    
    product_name = df_products[df_products['product_id'] == product_id]['product_name'].values[0]
    
    forecast_records.append({
        'product_id': product_id,
        'product_name': product_name,
        'avg_daily_demand': round(recent_avg_daily, 2),
        'forecast_next_30_days': projected_30_day_demand
    })

df_forecast = pd.DataFrame(forecast_records)
print("--- 30-Day Product Demand Forecast ---")
print(df_forecast)

# Save forecast to CSV for Power BI
df_forecast.to_csv('demand_forecast.csv', index=False)