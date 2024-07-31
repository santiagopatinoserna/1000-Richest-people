import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="1000 Richest People Insights", layout="wide")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('data/1000_richest_people_in_the_world.csv')
    # Remove duplicates based on 'Name' and keep the first occurrence
    df = df.drop_duplicates(subset=['Name'], keep='first')
    return df

df = load_data()

# Title
st.title("Insights from the 1000 Richest People Dataset")

# Sidebar
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect("Select Countries", df['Country'].unique())
selected_industries = st.sidebar.multiselect("Select Industries", df['Industry'].unique())

# Filter data
if selected_countries:
    df = df[df['Country'].isin(selected_countries)]
if selected_industries:
    df = df[df['Industry'].isin(selected_industries)]

# Main content
col1, col2 = st.columns(2)

with col1:
    # Top 10 richest people
    st.subheader("Top 10 Richest People")
    top_10 = df.nlargest(10, 'Net Worth (in billions)')
    fig_top10 = px.bar(top_10, x='Name', y='Net Worth (in billions)', 
                       hover_data=['Country', 'Industry', 'Company'],
                       color='Industry', title="Top 10 Richest People")
    st.plotly_chart(fig_top10, use_container_width=True)

    # Wealth distribution by industry
    st.subheader("Wealth Distribution by Industry")
    industry_wealth = df.groupby('Industry')['Net Worth (in billions)'].sum().sort_values(ascending=False)
    fig_industry = px.pie(industry_wealth, values='Net Worth (in billions)', names=industry_wealth.index,
                          title="Total Wealth by Industry")
    st.plotly_chart(fig_industry, use_container_width=True)

with col2:
    # Wealth distribution by country
    st.subheader("Wealth Distribution by Country")
    country_wealth = df.groupby('Country')['Net Worth (in billions)'].sum().sort_values(ascending=False)
    fig_country = px.bar(country_wealth, x=country_wealth.index, y='Net Worth (in billions)',
                         title="Total Wealth by Country")
    st.plotly_chart(fig_country, use_container_width=True)

    # Improved scatter plot: Net Worth vs Company (Top 20 companies)
    st.subheader("Net Worth vs Company (Top 20)")
    top_20_companies = df.groupby('Company')['Net Worth (in billions)'].sum().nlargest(20).index
    df_top_20 = df[df['Company'].isin(top_20_companies)]
    fig_scatter = px.scatter(df_top_20, x='Company', y='Net Worth (in billions)', color='Industry',
                             hover_data=['Name', 'Country'],
                             title="Net Worth vs Top 20 Companies (Colored by Industry)")
    fig_scatter.update_xaxes(categoryorder='total descending')
    fig_scatter.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_scatter, use_container_width=True)

# Additional insights
st.subheader("Key Insights")
col3, col4, col5 = st.columns(3)

with col3:
    total_wealth = df['Net Worth (in billions)'].sum()
    st.metric("Total Wealth", f"${total_wealth:.2f}B")

with col4:
    avg_wealth = df['Net Worth (in billions)'].mean()
    st.metric("Average Wealth", f"${avg_wealth:.2f}B")

with col5:
    num_countries = df['Country'].nunique()
    st.metric("Number of Countries", num_countries)

# Check if 'Age' column exists before creating the age distribution plot
if 'Age' in df.columns:
    st.subheader("Age Distribution of Billionaires")
    fig_age = px.histogram(df, x='Age', nbins=20, title="Age Distribution of Billionaires")
    st.plotly_chart(fig_age, use_container_width=True)
else:
    st.subheader("Distribution of Net Worth")
    fig_net_worth = px.histogram(df, x='Net Worth (in billions)', nbins=20, 
                                 title="Distribution of Net Worth (in billions)")
    st.plotly_chart(fig_net_worth, use_container_width=True)
    st.info("Age data is not available in the dataset. Showing Net Worth distribution instead.")

# Data table
st.subheader("Raw Data")
st.dataframe(df)