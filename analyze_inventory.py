import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('inventory_analytics.db')

# SQL query to analyze current stock versus reorder threshold and average daily sales
query = """
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    i.current_stock,
    i.reorder_point,
    ROUND(SUM(s.units_sold) / 365.0, 2) as avg_daily_sales,
    CASE 
        WHEN i.current_stock <= i.reorder_point THEN 'REORDER REQUIRED'
        ELSE 'SUFFICIENT STOCK'
    END as stock_status
FROM products p
JOIN current_inventory i ON p.product_id = i.product_id
JOIN daily_sales s ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name, p.category, i.current_stock, i.reorder_point
"""

df_analysis = pd.read_sql_query(query, conn)
print("--- Inventory Status & Reorder Analysis ---")
print(df_analysis[['product_name', 'current_stock', 'reorder_point', 'avg_daily_sales', 'stock_status']])

conn.close()