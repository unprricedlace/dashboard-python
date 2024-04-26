import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import requests
import pandas as pd
import json
import folium  # Add this import statement
from folium.plugins import MarkerCluster
# Create the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

# Define the color scheme
colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'dark-text': '#ffffff',
    'hover-bg': '#333333',
    'accent-color': '#FF851B'
}

# Define the layout of the dashboard
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1('Analytics Dashboard', style={'textAlign': 'center', 'color': colors['text'], 'fontFamily': 'Arial, sans-serif', 'fontSize': '36px', 'marginBottom': '20px'}),

    # KPIs section
    html.Div([
        html.Div([
            html.Div(id='total-downloads-container', style={'display': 'inline-block'}),
            html.Div(id='total-uploads-container', style={'display': 'inline-block', 'marginLeft': '20px'}),
            html.Div(id='total-verifications-container', style={'display': 'inline-block', 'marginLeft': '20px'}),
            html.Div(id='city-with-most-users-container', style={'display': 'inline-block'}),
            html.Div(id='users-favored-device-type-container', style={'display': 'inline-block', 'marginLeft': '20px'}),
        ], style={'marginBottom': '20px'}),
    ]),

    # Graphs and maps
   html.Div([


    dcc.Dropdown(
            id='graph-dropdown',
            options=[
                {'label': 'Monthly Verify', 'value': 'verify'},
                {'label': 'Monthly Downloads', 'value': 'downloads'},
                {'label': 'Monthly Uploads', 'value': 'uploads'}
            ],
            value=['downloads', 'uploads'],  # Default to 'verify' and 'downloads' selected
            multi=True,  # Allow multiple selection
            style={'width': '50%', 'margin': 'auto', 'marginBottom': '20px'}
        ),
        dcc.RangeSlider(
        id='year-range-slider',
        marks={i: str(i) for i in range(2019, 2025)},  # Range of years
        min=2019,
        max=2024,
        step=1,
        value=[2019, 2024],  # Default range
    ),


    dcc.Graph(id='monthly-user-count-graph'),
    dcc.Graph(id='verify-graph'),
    html.Div([
        dcc.Graph(id='activity-type-pie', style={'display': 'inline-block', 'width': '33%'}),
        dcc.Graph(id='department-pie', style={'display': 'inline-block', 'width': '33%'}),
        dcc.Graph(id='download-device-pie', style={'display': 'inline-block', 'width': '33%'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between'}),
    dcc.Graph(id='project-type-bar'),
    html.Iframe(id='city-map', style={'width': '100%', 'height': '600px', 'border': 'none'}),
], style={'marginTop': '20px'})
])

# Callbacks to update KPIs
@app.callback(
    Output('total-downloads-container', 'children'),
    [Input('total-downloads-container', 'id')]
)
def update_total_downloads(_):
    response = requests.get('http://localhost:5000/api/total_downloads')
    if response.status_code == 200:
        total_downloads_data = response.json()
        total_downloads = total_downloads_data['total_downloads']
        return html.Div([
            html.H3('Total Downloads:', style={'color': colors['text'], 'fontWeight': 'bold', 'fontFamily': 'Arial, sans-serif', 'fontSize': '24px'}),
            html.P(total_downloads, style={'color': colors['text'], 'fontFamily': 'Arial, sans-serif', 'fontSize': '20px'})
        ])
    else:
        return html.Div([
            html.H3('Error fetching data', style={'color': 'red'})
        ])

@app.callback(
    Output('total-uploads-container', 'children'),
    [Input('total-uploads-container', 'id')]
)
def update_total_uploads(_):
    response = requests.get('http://localhost:5000/api/total_uploads')
    if response.status_code == 200:
        total_uploads_data = response.json()
        total_uploads = total_uploads_data['total_uploads']
        return html.Div([
            html.H3('Total Uploads:', style={'color': colors['text'], 'fontWeight': 'bold', 'fontFamily': 'Arial, sans-serif', 'fontSize': '24px'}),
            html.P(total_uploads, style={'color': colors['text'], 'fontFamily': 'Arial, sans-serif', 'fontSize': '20px'})
        ])
    else:
        return html.Div([
            html.H3('Error fetching data', style={'color': 'red'})
        ])

@app.callback(
    Output('total-verifications-container', 'children'),
    [Input('total-verifications-container', 'id')]
)
def update_total_verifications(_):
    response = requests.get('http://localhost:5000/api/total_verifications')
    if response.status_code == 200:
        total_verifications_data = response.json()
        total_verifications = total_verifications_data['total_verifications']
        return html.Div([
            html.H3('Total Verifications:', style={'color': colors['text'], 'fontWeight': 'bold', 'fontFamily': 'Arial, sans-serif', 'fontSize': '24px'}),
            html.P(total_verifications, style={'color': colors['text'], 'fontFamily': 'Arial, sans-serif', 'fontSize': '20px'})
        ])
    else:
        return html.Div([
            html.H3('Error fetching data', style={'color': 'red'})
        ])

@app.callback(
    Output('city-with-most-users-container', 'children'),
    [Input('city-with-most-users-container', 'id')]
)
def update_city_with_most_users(_):
    response = requests.get('http://localhost:5000/api/city_with_most_users')
    if response.status_code == 200:
        city_with_most_users_data = response.json()
        city = city_with_most_users_data['city']
        user_count = city_with_most_users_data['user_count']
        return html.Div([
            html.H3('City with Most Users:', style={'color': colors['text'], 'fontWeight': 'bold', 'fontFamily': 'Arial, sans-serif', 'fontSize': '24px'}),
            html.P(f"{city} ({user_count} users)", style={'color': colors['text'], 'fontFamily': 'Arial, sans-serif', 'fontSize': '20px'})
        ])
    else:
        return html.Div([
            html.H3('Error fetching data', style={'color': 'red'})
        ])

@app.callback(
    Output('users-favored-device-type-container', 'children'),
    [Input('users-favored-device-type-container', 'id')]
)
def update_users_favored_device_type(_):
    response = requests.get('http://localhost:5000/api/users_favored_device_type')
    if response.status_code == 200:
        users_favored_device_type_data = response.json()
        users_favored_device_type = users_favored_device_type_data['users_favored_device_type']
        return html.Div([
            html.H3('Users Favored Device Type:', style={'color': colors['text'], 'fontWeight': 'bold', 'fontFamily': 'Arial, sans-serif', 'fontSize': '24px'}),
            html.P(users_favored_device_type, style={'color': colors['text'], 'fontFamily': 'Arial, sans-serif', 'fontSize': '20px'})
        ])
    else:
        return html.Div([
            html.H3('Error fetching data', style={'color': 'red'})
        ])





# Callbacks to update plots
# Callback to update the monthly user count graph
@app.callback(
    Output('monthly-user-count-graph', 'figure'),
    [
     Input('graph-dropdown', 'value'),
     Input('year-range-slider', 'value')]
)
def update_monthly_user_count_graph(selected_graphs , year_range):
    response = requests.get('http://localhost:5000/api/monthly_user_counts', params={'year_range': year_range})
    response_d = requests.get('http://localhost:5000/api/downloads', params={'year_range': year_range})
    response_u = requests.get('http://localhost:5000/api/upload', params={'year_range': year_range})
    response_v = requests.get('http://localhost:5000/api/verify', params={'year_range': year_range})


    print(selected_graphs)
    if response_d.status_code == 200:
        monthly_user_counts_json = response.json()
        downloads=response_d.json()
        upload=response_u.json()
        verify=response_v.json()
        monthly_user_counts = pd.DataFrame(monthly_user_counts_json)  # Assuming it's a list of dictionaries
        monthly_user_count_fig = px.line(monthly_user_counts, x='MonthYear', y='Username', title='Monthly User Count Over Time')
        monthly_user_count_fig.update_xaxes(title_text='Month-Year')
        monthly_user_count_fig.update_yaxes(title_text='User Count')
        monthly_user_count_fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['dark-text'], xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
        

       


         # Collect all figure objects

        if 'downloads' in selected_graphs and response_d.status_code==200:
            downloads_fig = px.line(downloads, x='MonthYear', y='Downloads', title='Monthly Downloads Over Time')
            downloads_fig.update_xaxes(title_text='Month-Year')
            downloads_fig.update_yaxes(title_text='Downloads Count')
            downloads_fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['dark-text'], xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
            return downloads_fig
                
    #         elif 'Uploads' in selected_graphs:
    #             monthly_user_count_fig = px.line(monthly_user_counts_data, x=monthly_user_counts_data['MonthYear'], y=monthly_user_counts_data['Uploads'], title='Monthly Uploads Over Time')
    #             monthly_user_count_fig.update_xaxes(title_text='Month-Year')
    #             monthly_user_count_fig.update_yaxes(title_text='Uploads Count')
    #             monthly_user_count_fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['dark-text'], xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
    #             figures.append(monthly_user_count_fig)
                
    #         elif 'Verify' in selected_graphs:
    #             monthly_user_count_fig = px.line(monthly_user_counts_data, x=monthly_user_counts_data['MonthYear'], y=monthly_user_counts_data['Verify'], title='Monthly Verify Activity Over Time')
    #             monthly_user_count_fig.update_xaxes(title_text='Month-Year')
    #             monthly_user_count_fig.update_yaxes(title_text='Verify Count')
    #             monthly_user_count_fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['dark-text'], xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
    #             figures.append(monthly_user_count_fig)
        
        # Return all figure objects
        
        return monthly_user_count_fig
    else:
        return {}





    # Callback to update Verify graph
@app.callback(
    Output('verify-graph', 'figure'), 
    [Input('verify-graph', 'hoverData'),
     Input('year-range-slider', 'value')]
)
def update_verify_graph(hoverData,year_range):
    # response = requests.get('http://localhost:5000/api/verify_graph_data')
    response = requests.get('http://localhost:5000/api/verify_graph_data', params={'year_range': year_range})
    if response.status_code == 200:
        verify_graph_data = response.json()
        verify_fig = px.bar(verify_graph_data, x='Username', y='Verify', hover_data=['Project'], color='Username')
        verify_fig.update_layout(title='Verify Activity', xaxis_title='Username', yaxis_title='Verify', plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['dark-text'], xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
        return verify_fig
    else:
        return {}

# Callback to update activity type pie chart
@app.callback(
    Output('activity-type-pie', 'figure'),
    [Input('verify-graph', 'hoverData'),
     Input('year-range-slider', 'value')]
)
def update_activity_type_pie(hoverData,year_range):
    response = requests.get('http://localhost:5000/api/activity_type_distribution', params={'year_range': year_range})
    if response.status_code == 200:
        activity_type_data = response.json()
        activity_type_pie_fig = px.pie(activity_type_data, names='Count', values='count', title='Activity Type Distribution')
        activity_type_pie_fig.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
        activity_type_pie_fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['dark-text'])
        return activity_type_pie_fig
    else:
        return {}

# Similar callbacks for department pie chart and download device pie chart

# Callback to update department pie chart
@app.callback(
    Output('department-pie', 'figure'),
    [Input('verify-graph', 'hoverData'),
     Input('year-range-slider', 'value')]
)
def update_department_pie(hoverData,year_range):
    response = requests.get('http://localhost:5000/api/department_distribution', params={'year_range': year_range})
    if response.status_code == 200:
        department_data = response.json()
        department_pie_fig = px.pie(department_data, names='Count', values='count', title='Department Distribution')
        department_pie_fig.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
        department_pie_fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['dark-text'])
        return department_pie_fig
    else:
        return {}

#update download device pie
@app.callback(
    Output('download-device-pie', 'figure'),
    [Input('verify-graph', 'hoverData'),
     Input('year-range-slider', 'value')]
)
def update_download_device_pie(hoverData,year_range):
    response = requests.get('http://localhost:5000/api/download_device_distribution', params={'year_range': year_range})
    if response.status_code == 200:
        response_json = response.content.decode('utf-8')  # Decode the response content to a JSON string
        download_device_data = pd.read_json(response_json)  # Convert JSON string to DataFrame
        print(download_device_data.columns)
        # download_device_data = pd.read_json(response.content)  # Convert JSON response to DataFrame
        download_device_pie_fig = px.pie(download_device_data, names='Count', values='count', title='Download Device Type Distribution')
        download_device_pie_fig.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
        download_device_pie_fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['dark-text'])
        return download_device_pie_fig
    else:
        return {}


dark_map_style = "cartodb dark_matter"
attribution = "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, Tiles courtesy of <a href='http://cartodb.com/attributions'>CartoDB</a>"
@app.callback(
    Output('city-map', 'srcDoc'),
    [Input('verify-graph', 'hoverData')]
)
def update_map(hoverData):
    # Make an API call to your backend to get the updated city_user_counts data
    response = requests.get('http://localhost:5000/api/city_user_counts')
    if response.status_code == 200:
        city_user_counts = response.json()  # Assuming your backend returns JSON data
        
        # Create a folium map
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, control_scale=True, tiles=dark_map_style, attr=attribution)

        # Add a marker cluster to the map
        marker_cluster = MarkerCluster().add_to(m)

        # Add markers for each city
        for city_data in city_user_counts:
            folium.Marker([city_data['Latitude'], city_data['Longitude']], 
                          popup=f"{city_data['City']}: {city_data['User Count']}").add_to(marker_cluster)

        # Return the HTML representation of the map
        return m._repr_html_()  # Assuming m is a folium map object
    else:
        return "<p>Failed to fetch data</p>"


@app.callback(
    Output('project-type-bar', 'figure'),
    [Input('verify-graph', 'hoverData')]
)
def update_project_type_bar(hoverData):
    # Make an API call to your backend to get the updated project type data
    response = requests.get('http://localhost:5000/api/project_type_data')
    if response.status_code == 200:
        project_type_data = response.json()  # Assuming your backend returns JSON data
        projects_per_type = pd.Series(project_type_data)  # Convert JSON data to pandas Series
        
        # Create the project type bar graph
        project_type_bar = px.bar(projects_per_type, x=projects_per_type.index, y=projects_per_type.values, title='Number of Projects by Project Type')
        project_type_bar.update_xaxes(title_text='Project Type', tickfont=dict(family='Arial, sans-serif', size=14))
        project_type_bar.update_yaxes(title_text='Number of Projects', tickfont=dict(family='Arial, sans-serif', size=14))
        project_type_bar.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['dark-text'], xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
        
        return project_type_bar
    else:
        return {}



# You can add more callbacks for other plots here

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
