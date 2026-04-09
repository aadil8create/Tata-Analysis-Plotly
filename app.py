import pandas as pd
import plotly.express as px
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Tata Motors Sales Dashboard", layout="wide")
st.title("Tata Motors Sales Performance Dashboard")

# 1. Data Collection & Preprocessing
@st.cache_data
def load_data():
    # Load the realistic Tata sales data
    df = pd.read_excel('Tata_Sales_Dataset.xlsx')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar Filters (Adds Interactivity)
st.sidebar.header("Filter Data")
selected_region = st.sidebar.multiselect(
    "Select Region", 
    options=df['Region'].unique(), 
    default=df['Region'].unique()
)
selected_fuel = st.sidebar.multiselect(
    "Select Fuel Type", 
    options=df['Fuel Type'].unique(), 
    default=df['Fuel Type'].unique()
)

# Apply filters to the dataframe
filtered_df = df[(df['Region'].isin(selected_region)) & (df['Fuel Type'].isin(selected_fuel))]

# 2. KPI Analysis
st.subheader("Key Performance Indicators")
col1, col2, col3 = st.columns(3)

total_revenue = filtered_df['Revenue'].sum()
total_units = filtered_df['Units Sold'].sum()
top_model = filtered_df.groupby('Model')['Units Sold'].sum().idxmax() if not filtered_df.empty else "N/A"

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Units Sold", f"{total_units:,}")
col3.metric("Top Selling Model", top_model)

st.divider()

# 3. Exploratory Data Analysis & Interactive Visualizations
col_chart1, col_chart2 = st.columns(2)

# Line Chart: Sales Trend Over Time
with col_chart1:
    monthly_sales = filtered_df.groupby('Date')['Units Sold'].sum().reset_index()
    fig_trend = px.line(
        monthly_sales, x='Date', y='Units Sold', markers=True, 
        title="Monthly Units Sold Trend",
        color_discrete_sequence=['#1f77b4']
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# Donut Chart: Segment Share
with col_chart2:
    segment_sales = filtered_df.groupby('Segment')['Units Sold'].sum().reset_index()
    fig_pie = px.pie(
        segment_sales, names='Segment', values='Units Sold', 
        title="Market Share by Vehicle Segment", hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Bar Chart: Model Comparison
model_sales = filtered_df.groupby('Model')['Units Sold'].sum().reset_index().sort_values(by='Units Sold', ascending=False)
fig_bar = px.bar(
    model_sales, x='Model', y='Units Sold', color='Model', 
    title="Total Units Sold by Vehicle Model",
    text_auto=True
)
st.plotly_chart(fig_bar, use_container_width=True)