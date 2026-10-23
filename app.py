import streamlit as st
import pandas as pd
import sqlite3
import os

st.set_page_config(page_title="Smart Inventory & Demand Forecasting", page_icon="📦", layout="wide")

st.title("📦 Smart Inventory & Demand Forecasting Dashboard")
st.markdown("An automated inventory management, stockout risk analysis, and demand forecasting pipeline.")

# Connect and load data from SQLite / CSVs
if os.path.exists('inventory_analytics.db'):
    conn = sqlite3.connect('inventory_analytics.db')
    
    # 1. Inventory Status Query
    query_inventory = """
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
    df_inventory = pd.read_sql_query(query_inventory, conn)
    
    # 2. Demand Forecast
    if os.path.exists('demand_forecast.csv'):
        df_forecast = pd.read_csv('demand_forecast.csv')
    else:
        df_forecast = pd.DataFrame()
        
    conn.close()

    # Tabs for UI
    tab1, tab2 = st.tabs(["📊 Inventory Stock & Reorder Status", "📈 30-Day Demand Forecast"])

    with tab1:
        st.subheader("Current Inventory & Reorder Risk Analysis")
        st.dataframe(df_inventory, use_container_width=True)
        
        # Highlight items needing reorder
        reorder_needed = df_inventory[df_inventory['stock_status'] == 'REORDER REQUIRED']
        if not reorder_needed.empty:
            st.warning(f"⚠️ Action Required: {len(reorder_needed)} products have fallen below their reorder threshold!")

    with tab2:
        st.subheader("30-Day Projected Demand")
        if not df_forecast.empty:
            st.dataframe(df_forecast, use_container_width=True)
            st.bar_chart(df_forecast.set_index('product_name')['forecast_next_30_days'])
        else:
            st.info("Demand forecast dataset not found.")

else:
    st.error("Database `inventory_analytics.db` not found. Please run your Python data pipeline scripts first.")