import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the initial theme
st.set_page_config(page_title="Global Terrorism Analysis", layout="wide", initial_sidebar_state="expanded")

# Define the custom CSS for light and dark themes
light_theme_css = """
    <style>
    .reportview-container {
        background-color: #ffffff;
        color: black;
    }
    .sidebar .sidebar-content {
        background-color: #f5f5f5;
        color: black;
    }
    .markdown-text-container {
        color: black;
    }
    .stButton > button {
        background-color: #e0e0e0;
        color: black;
    }
    .stSelectbox > div, .stRadio > div {
        color: black;
    }
    </style>
"""

dark_theme_css = """
    <style>
    .reportview-container {
        background-color: #2e2e2e;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #333;
        color: white;
    }
    .markdown-text-container {
        color: white;
    }
    .stButton > button {
        background-color: #444;
        color: white;
    }
    .stSelectbox > div, .stRadio > div {
        color: white;
    }
    </style>
"""

# Set the title of the Streamlit app
st.title("Global Terrorism Analysis")

# Description
st.markdown("""
This application provides an interactive interface to explore the Global Terrorism dataset.
You can view various plots and insights extracted from the data.
""", unsafe_allow_html=True)

# Add a theme toggle to the sidebar
theme = st.sidebar.radio("Select Theme", ["Light", "Dark"])

# Apply theme based on user selection
if theme == "Dark":
    st.markdown(dark_theme_css, unsafe_allow_html=True)
else:
    st.markdown(light_theme_css, unsafe_allow_html=True)

# Load the dataset (update the path to where your dataset is located)
@st.cache_data
def load_data():
    df = pd.read_excel("globalterrorism.xlsx")

    # Extract and rename relevant columns
    df = df[['iyear', 'country_txt', 'region_txt', 'city', 'attacktype1_txt', 'targtype1_txt', 'gname', 'nkill']]
    df.rename(columns={
        'iyear': 'year',
        'country_txt': 'country',
        'region_txt': 'region',
        'attacktype1_txt': 'attacktype',
        'targtype1_txt': 'target',
        'gname': 'organization',
        'nkill': 'killed'
    }, inplace=True)

    # Drop rows with missing values and clean the data
    df = df.dropna()
    df = df.astype({'killed': 'int'})
    return df

data = load_data()

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox(
    "Choose a visualization",
    ["Dataset Overview", "Year-wise Attacks", "Region and Year-wise Terrorist Attacks", "Region-wise Attacks", 
     "Top 10 Affected Countries", "Attack Methods", "Most Active Terrorist Organizations", 
     "Top 10 Countries - People Killed", "Most Affected Cities", "North America Killings", 
     "South Asia Killings", "Middle East Killings", "Top 10 Terrorist Organizations", 
     "Top 5 Targets", "Top 5 Deadliest Years"]
)

# Display different visualizations based on the selection
if page == "Dataset Overview":
    st.subheader("Dataset Overview")
    st.dataframe(data.head())
    st.write("Number of rows and columns:", data.shape)

elif page == "Year-wise Attacks":
    st.subheader("Year-wise Terrorist Attacks")

    # Group data by year and count the number of attacks
    yearly_attacks = data.groupby('year').size()

    plt.figure(figsize=(14, 7))  # Increase the size for better clarity
    sns.lineplot(x=yearly_attacks.index, y=yearly_attacks.values, marker='o', color='red', linewidth=2)

    # Customize the plot
    plt.title('Number of Terrorist Attacks per Year', fontsize=18, weight='bold')
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Attacks', fontsize=14)
    plt.xticks(ticks=yearly_attacks.index, rotation=45)  # Display each year on the x-axis with a 45-degree rotation
    plt.grid(True)  # Add grid

    # Add some additional customization
    plt.fill_between(yearly_attacks.index, yearly_attacks.values, color='red', alpha=0.1)  # Add area fill under the line
    plt.axhline(y=yearly_attacks.mean(), color='blue', linestyle='--', linewidth=1, label=f'Average Attacks ({yearly_attacks.mean():.2f})')  # Add horizontal line for average attacks
    plt.legend()

    st.pyplot(plt)

elif page == "Region and Year-wise Terrorist Attacks":
    st.subheader("Region and Year-wise Terrorist Attacks")

    # Create a crosstab for the region and year data
    region_year_crosstab = pd.crosstab(data.year, data.region)

    plt.figure(figsize=(8, 6))  # Set the figure size
    region_year_crosstab.plot(kind='area', stacked=True, figsize=(8, 6), alpha=0.8)  # Create an area plot

    # Customize the plot
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.title('Terrorist Activities by Region in each Year', fontsize=18, weight='bold')
    plt.grid(True)  # Add grid
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    st.pyplot(plt)  # Display the plot in Streamlit

elif page == "Region-wise Attacks":
    st.subheader("Region-wise Terrorist Attacks")

    # Group data by region and count the number of attacks
    region_attacks = data.groupby('region').size().sort_values(ascending=False).reset_index()
    region_attacks.columns = ['region', 'count']  # Rename columns for clarity

    # Define custom colors for each bar
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'gray', 'cyan']

    # Plot the bar plot with grid and custom colors
    plt.figure(figsize=(8, 6))
    sns.barplot(x='count', y='region', data=region_attacks, palette=colors[:len(region_attacks)], ec='black')
    plt.title('Number of Terrorist Attacks by Region', fontsize=16)
    plt.xlabel('Number of Attacks', fontsize=14)
    plt.ylabel('Region', fontsize=14)
    plt.grid(True)  # Add grid to the plot

    st.pyplot(plt)

elif page == "Top 10 Affected Countries":
    st.subheader("Top 10 Affected Countries")

    # Get the top 10 countries affected by terrorism
    top_countries = data['country'].value_counts().head(10).reset_index()
    top_countries.columns = ['country', 'count']  # Rename columns for clarity

    # Define custom colors for each bar
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'gray', 'cyan']

    # Plot the bar plot with grid and custom colors
    plt.figure(figsize=(8, 6))
    sns.barplot(x='count', y='country', data=top_countries, palette=colors, ec='black')
    plt.title('Top 10 Countries Affected by Terrorism', fontsize=16)
    plt.xlabel('Number of Attacks', fontsize=14)
    plt.ylabel('Country', fontsize=14)
    plt.grid(True)  # Add grid to the plot

    st.pyplot(plt)

elif page == "Attack Methods":
    st.subheader("Attack Methods Used")

    # Count the occurrences of each attack method
    attack_methods = data['attacktype'].value_counts().reset_index()
    attack_methods.columns = ['attack_method', 'count']  # Rename columns for clarity

    # Plot the bar plot with grid and red color for bars
    plt.figure(figsize=(8, 6))
    sns.barplot(x='count', y='attack_method', data=attack_methods, color='red', ec='black')
    plt.title('Types of Attack Methods', fontsize=16)
    plt.xlabel('Number of Attacks', fontsize=14)
    plt.ylabel('Attack Method', fontsize=14)
    plt.grid(True)  # Add grid to the plot

    st.pyplot(plt)

elif page == "Most Active Terrorist Organizations":
    st.subheader("Most Active Terrorist Organizations")

    # Get the top 10 organizations
    g_type = data['organization'].value_counts().reset_index()
    g_type.columns = ['organization_name', 'count']  # Rename columns for clarity
    g_type = g_type.head(10)

    # Plot the bar plot with grid and custom colors
    plt.figure(figsize=(8, 6))
    sns.barplot(x='count', y='organization_name', data=g_type, palette='viridis', ec='black')
    plt.title('Top 10 Most Active Terrorist Organizations', fontsize=16)
    plt.xlabel('Number of Attacks', fontsize=14)
    plt.ylabel('Organization', fontsize=14)
    plt.grid(True)  # Add grid to the plot

    st.pyplot(plt)

elif page == "Top 10 Countries - People Killed":
    st.subheader("Top 10 Countries by Number of People Killed")

    # Count the total number of people killed by country
    country_kills = data.groupby('country')['killed'].sum().reset_index().sort_values(by='killed', ascending=False).head(10)
    
    # Define custom colors for each bar
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'gray', 'cyan']

    # Plot the bar plot with grid and custom colors
    plt.figure(figsize=(8, 6))
    sns.barplot(x='killed', y='country', data=country_kills, palette=colors, ec='black')
    plt.title('Top 10 Countries by Number of People Killed', fontsize=16)
    plt.xlabel('Number of People Killed', fontsize=14)
    plt.ylabel('Country', fontsize=14)
    plt.grid(True)  # Add grid to the plot

    st.pyplot(plt)

elif page == "Most Affected Cities":
    st.subheader("Most Affected Cities")

    # Get the top 10 cities affected by terrorism
    top_cities = data['city'].value_counts().head(10).reset_index()
    top_cities.columns = ['city', 'count']  # Rename columns for clarity

    # Define custom colors for each bar
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'gray', 'cyan']

    # Plot the bar plot with grid and custom colors
    plt.figure(figsize=(8, 6))
    sns.barplot(x='count', y='city', data=top_cities, palette=colors, ec='black')
    plt.title('Top 10 Most Affected Cities', fontsize=16)
    plt.xlabel('Number of Attacks', fontsize=14)
    plt.ylabel('City', fontsize=14)
    plt.grid(True)  # Add grid to the plot

    st.pyplot(plt)

elif page == "North America Killings":
    st.subheader("North America - Total Killings")

    # Filter data for North America
    north_america_data = data[data['region'] == 'North America']

    # Plot total killings by country in North America
    plt.figure(figsize=(10, 6))
    sns.barplot(x='country', y='killed', data=north_america_data.groupby('country')['killed'].sum().reset_index().sort_values(by='killed', ascending=False), color='blue', ec='black')
    plt.xticks(rotation=45)
    plt.title('Total Killings by Country in North America', fontsize=16)
    plt.xlabel('Country', fontsize=14)
    plt.ylabel('Total Killings', fontsize=14)
    plt.grid(True)  # Add grid to the plot

    st.pyplot(plt)

elif page == "South Asia Killings":
    st.subheader("South Asia - Total Killings")

    # Filter data for South Asia
    south_asia_data = data[data['region'] == 'South Asia']

    # Plot total killings by country in South Asia
    plt.figure(figsize=(10, 6))
    sns.barplot(x='country', y='killed', data=south_asia_data.groupby('country')['killed'].sum().reset_index().sort_values(by='killed', ascending=False), color='green', ec='black')
    plt.xticks(rotation=45)
    plt.title('Total Killings by Country in South Asia', fontsize=16)
    plt.xlabel('Country', fontsize=14)
    plt.ylabel('Total Killings', fontsize=14)
    plt.grid(True)  # Add grid to the plot

    st.pyplot(plt)

elif page == "Middle East Killings":
    st.subheader("Middle East - Total Killings")

    # Filter data for the Middle East
    middle_east_data = data[data['region'] == 'Middle East']

    # Plot total killings by country in the Middle East
    plt.figure(figsize=(10, 6))
    sns.barplot(x='country', y='killed', data=middle_east_data.groupby('country')['killed'].sum().reset_index().sort_values(by='killed', ascending=False), color='purple', ec='black')
    plt.xticks(rotation=45)
    plt.title('Total Killings by Country in the Middle East', fontsize=16)
    plt.xlabel('Country', fontsize=14)
    plt.ylabel('Total Killings', fontsize=14)
    plt.grid(True)  # Add grid to the plot

    st.pyplot(plt)

elif page == "Top 10 Terrorist Organizations":
    st.subheader("Top 10 Terrorist Organizations")

    # Get the top 10 terrorist organizations by the number of attacks
    top_orgs = data['organization'].value_counts().head(10).reset_index()
    top_orgs.columns = ['organization', 'count']  # Rename columns for clarity

    # Define custom colors for each bar
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'gray', 'cyan']

    # Plot the bar plot with grid and custom colors
    plt.figure(figsize=(8, 6))
    sns.barplot(x='count', y='organization', data=top_orgs, palette=colors, ec='black')
    plt.title('Top 10 Terrorist Organizations by Number of Attacks', fontsize=16)
    plt.xlabel('Number of Attacks', fontsize=14)
    plt.ylabel('Organization', fontsize=14)
    plt.grid(True)  # Add grid to the plot

    st.pyplot(plt)

elif page == "Top 5 Targets":
    st.subheader("Top 5 Targets")

    # Get the top 5 targets by the number of attacks
    top_targets = data['target'].value_counts().head(5).reset_index()
    top_targets.columns = ['target', 'count']  # Rename columns for clarity

    # Define custom colors for each bar
    colors = ['red', 'orange', 'yellow', 'green', 'blue']

    # Plot the bar plot with grid and custom colors
    plt.figure(figsize=(8, 6))
    sns.barplot(x='count', y='target', data=top_targets, palette=colors, ec='black')
    plt.title('Top 5 Targets by Number of Attacks', fontsize=16)
    plt.xlabel('Number of Attacks', fontsize=14)
    plt.ylabel('Target', fontsize=14)
    plt.grid(True)  # Add grid to the plot

    st.pyplot(plt)

elif page == "Top 5 Deadliest Years":
    st.subheader("Top 5 Deadliest Years")

    # Get the top 5 deadliest years by the number of people killed
    top_years = data.groupby('year')['killed'].sum().reset_index().sort_values(by='killed', ascending=False).head(5)

    # Define custom colors for each bar
    colors = ['red', 'orange', 'yellow', 'green', 'blue']

    # Plot the bar plot with grid and custom colors
    plt.figure(figsize=(8, 6))
    sns.barplot(x='year', y='killed', data=top_years, palette=colors, ec='black')
    plt.title('Top 5 Deadliest Years by Number of People Killed', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of People Killed', fontsize=14)
    plt.grid(True)  # Add grid to the plot

    st.pyplot(plt)

