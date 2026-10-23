import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# 1. Generate Products Metadata
products = [
    {'product_id': 'PROD_001', 'product_name': 'Wireless Headphones', 'category': 'Electronics', 'unit_cost': 45.0, 'selling_price': 89.99, 'lead_time_days': 5},
    {'product_id': 'PROD_002', 'product_name': 'Ergonomic Chair', 'category': 'Furniture', 'unit_cost': 120.0, 'selling_price': 249.99, 'lead_time_days': 10},
    {'product_id': 'PROD_003', 'product_name': 'Mechanical Keyboard', 'category': 'Electronics', 'unit_cost': 35.0, 'selling_price': 79.99, 'lead_time_days': 7},
    {'product_id': 'PROD_004', 'product_name': 'Stainless Steel Water Bottle', 'category': 'Home & Kitchen', 'unit_cost': 8.0, 'selling_price': 24.99, 'lead_time_days': 3},
    {'product_id': 'PROD_005', 'product_name': 'Standing Desk', 'category': 'Furniture', 'unit_cost': 210.0, 'selling_price': 450.00, 'lead_time_days': 14}
]

df_products = pd.DataFrame(products)

# 2. Generate Daily Historical Sales (1 Year of Data)
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
date_range = pd.date_range(start_date, end_date, freq='D')

sales_records = []

for date in date_range:
    for p in products:
        # Base demand with seasonal variation + noise
        base_demand = np.random.randint(10, 50)
        # Weekend boost
        if date.weekday() >= 5:
            base_demand = int(base_demand * 1.3)
        
        units_sold = max(0, base_demand)
        revenue = round(units_sold * p['selling_price'], 2)
        
        sales_records.append({
            'date': date.strftime('%Y-%m-%d'),
            'product_id': p['product_id'],
            'units_sold': units_sold,
            'revenue': revenue
        })

df_sales = pd.DataFrame(sales_records)

# 3. Generate Current Inventory Levels
inventory_records = []
for p in products:
    current_stock = np.random.randint(50, 400)
    inventory_records.append({
        'product_id': p['product_id'],
        'current_stock': current_stock,
        'reorder_point': int(p['lead_time_days'] * 25), # Working threshold
        'last_restock_date': '2025-12-15'
    })

df_inventory = pd.DataFrame(inventory_records)

# Save to CSV
df_products.to_csv('products.csv', index=False)
df_sales.to_csv('daily_sales.csv', index=False)
df_inventory.to_csv('current_inventory.csv', index=False)

print("Inventory & Sales Datasets Generated Successfully!")
print("Saved: products.csv, daily_sales.csv, current_inventory.csv")