import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import BytesIO

# Set the title of the Streamlit app
st.title("Global Terrorism Analysis")

# Description
st.markdown("""
This application provides an interactive interface to explore the Global Terrorism dataset.
You can view various plots and insights extracted from the data.
""")

# URL of the raw file
url = 'https://github.com/GayasuddinMohd/Global-Terrorism-Patterns-A-Data-Analysis-Perspective/raw/main/globalterrorism.xlsx'

# Download the file
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Load the Excel file into a pandas DataFrame
df = pd.read_excel(BytesIO(response.content))

# Display the raw data in Streamlit
st.write(df)

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

# Display the cleaned data in Streamlit
st.write(df)

# You can now add more analysis and visualizations here

data = load_data()

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox(
    "Choose a visualization",
    ["Dataset Overview", "Year-wise Attacks","Region and Year-wise Terrorist Attacks" ,"Region-wise Attacks", "Top 10 Affected Countries", "Attack Methods",
     "Most Active Terrorist Organizations",
     "Top 10 Countries - People Killed", "Most Affected Cities", "North America Killings", "South Asia Killings",
     "Middle East Killings", "Top 10 Terrorist Organizations", "Top 5 Targets", "Top 5 Deadliest Years"]
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
    plt.fill_between(yearly_attacks.index, yearly_attacks.values, color='red',
                     alpha=0.1)  # Add area fill under the line
    plt.axhline(y=yearly_attacks.mean(), color='blue', linestyle='--', linewidth=1,
                label=f'Average Attacks ({yearly_attacks.mean():.2f})')  # Add horizontal line for average attacks
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

    # Create `g_type` by counting the occurrences of each organization
    g_type = data['organization'].value_counts().reset_index()
    g_type.columns = ['organization_name', 'count']  # Rename columns for clarity

    # Sort and select top 10 most active terrorist organizations
    top_organizations = g_type.sort_values(by='count', ascending=False).head(10)

    plt.figure(figsize=(10, 5))
    sns.barplot(x='organization_name', y='count', data=top_organizations, ec='black', palette='flare')
    plt.title('Most Active Terrorist Organizations in the World', fontsize=20)
    plt.xlabel('Organization Name', fontsize=15)
    plt.ylabel('Count', fontsize=15)
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.grid(True)

    st.pyplot(plt)

elif page == "Top 10 Countries - People Killed":
    st.subheader("Top 10 Countries Where Most People Were Killed")
    top10_c = data.groupby('country')['killed'].sum().sort_values(ascending=False).head(10).reset_index()

    plt.figure(figsize=(10, 5))
    sns.barplot(y='killed', x='country', data=top10_c, ec='black')
    plt.xlabel('Country')
    plt.ylabel('Number of People Killed')
    plt.grid(True)
    st.pyplot(plt)

elif page == "Most Affected Cities":
    st.subheader("Most Affected Cities")

    # Ensure the correct column name is used and the data is aggregated properly
    top_cities = data['city'].value_counts().head(10).reset_index()
    top_cities.columns = ['city', 'count']  # Renaming columns for clarity

    plt.figure(figsize=(10, 5))
    sns.barplot(x='city', y='count', data=top_cities, ec='black', palette='Set3')
    plt.title("Most Affected Cities in the World", fontsize=15)
    plt.xlabel('City', fontsize=12)
    plt.ylabel("Number of Attacks", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    st.pyplot(plt)

elif page == "North America Killings":
    st.subheader("Number of People Killed in North America Over the Years")
    a_a = data[(data['region'].isin(['North America']))].groupby(['year', 'country'])['killed'].sum().reset_index()

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=a_a, x='year', y='killed', hue='country', style='country', palette='magma_r', markers=True,
                 dashes=False)
    plt.title("Total People Killed in North America Over the Years")
    plt.xlabel('Year')
    plt.ylabel('Number of People Killed')
    plt.grid(True)
    st.pyplot(plt)

elif page == "South Asia Killings":
    st.subheader("Number of People Killed in South Asia Over the Years")
    a_a = \
    data[(data['region'].isin(['South Asia'])) & (data['country'].isin(['Pakistan', 'Afghanistan', 'India']))].groupby(
        ['year', 'country'])['killed'].sum().reset_index()

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=a_a, x='year', y='killed', hue='country', style='country', palette='magma_r', markers=True,
                 dashes=False)
    plt.title("Total People Killed in Pakistan, Afghanistan, and India Over the Years")
    plt.xlabel('Year')
    plt.ylabel('Number of People Killed')
    plt.grid(True)
    st.pyplot(plt)

elif page == "Middle East Killings":
    st.subheader("Number of People Killed in the Middle East Over the Years")
    a_a = \
    data[(data['region'].isin(['Middle East & North Africa'])) & (data['country'].isin(['Iraq', 'Syria']))].groupby(
        ['year', 'country'])['killed'].sum().reset_index()

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=a_a, x='year', y='killed', hue='country', style='country', palette='magma_r', markers=True,
                 dashes=False)
    plt.title("Total People Killed in Iraq and Syria Over the Years")
    plt.xlabel('Year')
    plt.ylabel('Number of People Killed')
    plt.grid(True)
    st.pyplot(plt)

elif page == "Top 10 Terrorist Organizations":
    st.subheader("Top 10 Terrorist Organizations")

    # Ensure the correct column name is used
    top_organizations = data['organization'].value_counts().head(10).reset_index()
    top_organizations.columns = ['organization', 'count']  # Renaming columns for clarity

    plt.figure(figsize=(10,5))  # Increase the height of the plot for better readability
    sns.barplot(x='organization', y='count', data=top_organizations, ec='black', lw=1)

    plt.xlabel('Organization', fontsize=12)
    plt.ylabel('Number of Attacks', fontsize=12)
    plt.title('Top 10 Terrorist Organizations by Number of Attacks', fontsize=16)

    plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate x-axis labels for clarity
    plt.grid(True)
    st.pyplot(plt)

elif page == "Top 5 Targets":
    st.subheader("Top 5 Targets of Terrorists")
    top_targets = data['target'].value_counts().head(5)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=top_targets.index, y=top_targets.values, palette=['red', 'yellow', 'green', 'black', 'pink'],
                ec='black')
    plt.xlabel('Target')
    plt.ylabel('Number of Attacks')
    plt.grid(True)
    st.pyplot(plt)

elif page == "Top 5 Deadliest Years":
    st.subheader("Top 5 Deadliest Years")
    year_killed = data.groupby('year')['killed'].sum().sort_values(ascending=False).head(5).reset_index()

    plt.figure(figsize=(10, 5))
    sns.barplot(x='year', y='killed', data=year_killed, palette=['red', 'orange', 'pink', 'blue', 'yellow'], ec='black')
    plt.xlabel('Year')
    plt.ylabel('Number of People Killed')
    plt.grid(True)
    st.pyplot(plt)

# Footer
st.sidebar.info("© 2024 Global Terrorism Analysis")
