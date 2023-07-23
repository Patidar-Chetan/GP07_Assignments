#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module=".*dash_core_components.*")
warnings.filterwarnings("ignore", category=UserWarning, module=".*dash_html_components.*")


# URL of the webpage containing the table
url = "http://www.tobaccopreventioncessation.com/Tobacco-use-among-Indian-states-Key-findings-from-the-latest-demographic-health-survey,132466,0,2.html"

# Send an HTTP GET request to the webpage
response = requests.get(url)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table on the webpage based on the class name 'table-wrap'
table = soup.find('div', class_='table-wrap')

# Extract the table data into a list of lists
table_data = []
for row in table.find_all('tr')[2:]:  # Skip the header row
    cols = row.find_all('td')
    cols = [col.text.strip() for col in cols]
    table_data.append(cols)

# Create a DataFrame from the table data
df = pd.DataFrame(table_data, columns=["State", "NFHS-5 (2019–20)", "GATS (2016–17)", "Men", "Women"])

# Fill the missing values in "Men" and "Women" columns using "NFHS-5 (2019–20)" data
df['Men'] = df['Men'].combine_first(df['NFHS-5 (2019–20)'])
df['Women'] = df['Women'].combine_first(df['NFHS-5 (2019–20)'])

# Drop the "NFHS-5 (2019–20)" and "GATS (2016–17)" columns
df.drop(columns=['NFHS-5 (2019–20)', 'GATS (2016–17)'], inplace=True)

# Sort the DataFrame by 'Men' and 'Women' columns in descending order
df.sort_values(by=['Men', 'Women'], ascending=[False, False], inplace=True)

# Create the Dash app
app = dash.Dash(__name__)

# Create a bar chart for male tobacco consumption
fig_male = px.bar(df, x='State', y='Men', title='Male Tobacco Consumption in Indian States', color='Men')

# Create a bar chart for female tobacco consumption
fig_female = px.bar(df, x='State', y='Women', title='Female Tobacco Consumption in Indian States', color='Women')

# Layout of the dashboard
app.layout = html.Div([
    html.H1('Tobacco Consumption in Indian States', style={'text-align': 'center'}),
    
    dcc.Graph(id='male-plot', figure=fig_male),
    
    dcc.Graph(id='female-plot', figure=fig_female)
])

if __name__ == '__main__':
    app.run_server(debug=True)

