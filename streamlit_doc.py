import streamlit as st
import pandas as pd
import plotly.express as px

# Load and clean data
df = pd.read_csv('startup_funding.csv')

# Clean column names (optional)
df.columns = df.columns.str.strip()

# Remove commas, NaNs and convert funding to numeric
df['Amount in USD'] = pd.to_numeric(df['Amount in USD'].str.replace(',', '').str.strip(), errors='coerce')
df.dropna(subset=['Amount in USD', 'Startup Name'], inplace=True)

# Sidebar
st.sidebar.title('Startup Analysis')
option = st.sidebar.selectbox('Select one', ['Overall Analysis', 'Startup', 'Investors'])

if option == 'Overall Analysis':
    st.title('📊 Overall Funding Analysis')

    # Top 10 funded startups
    top_funded = df.groupby('Startup Name')['Amount in USD'].sum().sort_values(ascending=False).head(10).reset_index()

    # Pie Chart
    st.subheader("Top 10 Funded Startups (Pie Chart)")
    fig_pie = px.pie(top_funded,
                     names='Startup Name',
                     values='Amount in USD',
                     title='Funding Distribution (Top 10 Startups)',
                     hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

    # Bar Chart
    st.subheader("Top 10 Funded Startups (Bar Chart)")
    fig_bar = px.bar(top_funded,
                     x='Startup Name',
                     y='Amount in USD',
                     color='Startup Name',
                     title='Top 10 Funded Startups',
                     text_auto='.2s')
    st.plotly_chart(fig_bar, use_container_width=True)

elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select a Startup', df['Startup Name'].dropna().unique())
    st.title(f'📈 Funding Analysis: {selected_startup}')
    filtered_df = df[df['Startup Name'] == selected_startup]
    st.dataframe(filtered_df)

#else:
    #selected_investor = st.sidebar.selectbox('Select Investor Type', ['Totally Invested', 'Partially Invested', 'Small Amount'])
    #st.title(f'💰 Investors Analysis: {selected_investor}')
