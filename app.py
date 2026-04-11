import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.data_service import load_and_clean_data

# ==========================================
# 1. PAGE CONFIGURATION 
# ==========================================
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")
st.title("Retail Sales Insights")
st.markdown("Interactive sales dashboard. Use the filters to explore market performance and customer behavior.")

# ==========================================
# 2. DATA LOADING 
# ==========================================
@st.cache_data
def fetch_data():
    return load_and_clean_data()

with st.spinner("Initializing data pipeline..."):
    df = fetch_data()

# ==========================================
# 3. INTERACTIVE SIDEBAR FILTERS
# ==========================================
st.sidebar.header("Filters")

min_date = df['Order Date'].min().date()
max_date = df['Order Date'].max().date()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

all_regions = df['Region'].unique()
selected_regions = st.sidebar.multiselect("Region", all_regions, default=all_regions)

all_categories = df['Category'].unique()
selected_categories = st.sidebar.multiselect("Product Category", all_categories, default=all_categories)

# Apply filters
if len(date_range) == 2:
    mask = (df['Order Date'].dt.date >= date_range[0]) & \
           (df['Order Date'].dt.date <= date_range[1]) & \
           (df['Region'].isin(selected_regions)) & \
           (df['Category'].isin(selected_categories))
    filtered_df = df[mask]
else:
    filtered_df = df

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ==========================================
# 4. HIGH-LEVEL METRICS
# ==========================================
st.markdown("---")
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Total Revenue", f"${filtered_df['Sales'].sum():,.0f}")
metric_col2.metric("Total Orders", f"{filtered_df['Order ID'].nunique():,}")
metric_col3.metric("Average Order Value", f"${filtered_df['Sales'].mean():,.2f}")
st.markdown("---")

# ==========================================
# 5. DASHBOARD CHARTS
# ==========================================
sns.set_theme(style="whitegrid") # Ensures all charts look uniform

# ROW 1: Category Sales & Region Share
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Product Category")
    category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
    category_sales = category_sales.sort_values(by='Sales', ascending=False)
    
    fig_cat, ax_cat = plt.subplots(figsize=(6, 4))
    sns.barplot(data=category_sales, x='Category', y='Sales', palette='viridis', ax=ax_cat)
    for container in ax_cat.containers:
        ax_cat.bar_label(container, fmt='${:,.0f}')
    plt.tight_layout()
    st.pyplot(fig_cat)

with col2:
    st.subheader("Market Share by Region")
    region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
    
    fig_reg, ax_reg = plt.subplots(figsize=(6, 4))
    colors = sns.color_palette('pastel')[0:len(region_sales)]
    ax_reg.pie(region_sales['Sales'], labels=region_sales['Region'], colors=colors, 
            autopct='%1.1f%%', startangle=140, pctdistance=0.85, 
            textprops={'fontsize': 10, 'weight': 'bold'})
    
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    fig_reg.gca().add_artist(centre_circle)
    plt.tight_layout()
    st.pyplot(fig_reg)

st.markdown("---")

# ROW 2: Customer Behavior & Top Products
col3, col4 = st.columns(2)

with col3:
    st.subheader("Revenue by Customer Segment")
    segment_sales = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
    segment_sales = segment_sales.sort_values(by='Sales', ascending=False)
    
    fig_seg, ax_seg = plt.subplots(figsize=(6, 4))
    sns.barplot(data=segment_sales, x='Segment', y='Sales', palette='coolwarm', ax=ax_seg)
    for container in ax_seg.containers:
        ax_seg.bar_label(container, fmt='${:,.0f}', padding=3)
    plt.tight_layout()
    st.pyplot(fig_seg)

with col4:
    st.subheader("Top 10 Sub-Categories")
    subcat_sales = filtered_df.groupby('Sub-Category')['Sales'].sum().reset_index()
    subcat_sales = subcat_sales.sort_values(by='Sales', ascending=False).head(10)

    fig_sub, ax_sub = plt.subplots(figsize=(6, 4))
    sns.barplot(data=subcat_sales, y='Sub-Category', x='Sales', palette='magma', ax=ax_sub)
    for container in ax_sub.containers:
        ax_sub.bar_label(container, fmt='${:,.0f}', padding=3)
    plt.tight_layout()
    st.pyplot(fig_sub)