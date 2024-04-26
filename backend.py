from flask import Flask, jsonify,request
import pandas as pd

app = Flask(__name__)

# Read data from CSV
df = pd.read_csv("data2.csv", encoding='latin1')
print(df["Download_Device_Type"])

# Calculate KPIs
total_downloads = df['Downloads'].sum()
total_uploads = df['Upload'].sum()
total_verifications = df['Verify'].sum()

# Convert int64 type to standard Python types
total_downloads = int(total_downloads)
total_uploads = int(total_uploads)
total_verifications = int(total_verifications)

city_user_counts = df.groupby('City')['Username'].nunique().reset_index()
city_with_most_users = city_user_counts.loc[city_user_counts['Username'].idxmax()]
users_favored_device_type = df['Download_Device_Type'].value_counts().idxmax()

projects_per_type = df['Project'].value_counts()




@app.route('/api/total_downloads')
def get_total_downloads():
    return jsonify({'total_downloads': total_downloads})

@app.route('/api/total_uploads')
def get_total_uploads():
    return jsonify({'total_uploads': total_uploads})

@app.route('/api/total_verifications')
def get_total_verifications():
    return jsonify({'total_verifications': total_verifications})

@app.route('/api/city_with_most_users')
def get_city_with_most_users():
    return jsonify({
        'city': city_with_most_users['City'],
        'user_count': int(city_with_most_users['Username'])  # Convert to int
    })

@app.route('/api/users_favored_device_type')
def get_users_favored_device_type():
    return jsonify({'users_favored_device_type': users_favored_device_type})

@app.route('/api/projects_per_type')
def get_projects_per_type():
    return projects_per_type.to_json()

@app.route('/api/monthly_user_counts')
def get_monthly_user_counts():

    year_range = request.args.getlist('year_range')  # Get the year range from the request query parameters as a list
    if len(year_range) != 2:
        return "Invalid year range", 400  # Return a 400 Bad Request if the year range is invalid

    # Parse the year range strings into integers
    start_year = int(year_range[0])
    end_year = int(year_range[1])

    # Filter data based on the year range
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['MonthYear'] = df['Timestamp'].dt.to_period('M')
    df['MonthYear'] = df['MonthYear'].astype(str)
    filtered_df = df[df['MonthYear'].str[:4].astype(int).between(start_year, end_year)]
    monthly_user_counts = filtered_df.groupby('MonthYear')['Username'].nunique().reset_index()
    monthly_user_counts['MonthYear'] = monthly_user_counts['MonthYear'].astype(str)
    return monthly_user_counts.to_json(orient='records')


@app.route('/api/downloads')
def get_monthly_downloads():

    year_range = request.args.getlist('year_range')  # Get the year range from the request query parameters as a list
    if len(year_range) != 2:
        return "Invalid year range", 400  # Return a 400 Bad Request if the year range is invalid

    # Parse the year range strings into integers
    start_year = int(year_range[0])
    end_year = int(year_range[1])

    # Filter data based on the year range
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['MonthYear'] = df['Timestamp'].dt.to_period('M')
    df['MonthYear'] = df['MonthYear'].astype(str)
    filtered_df = df[df['MonthYear'].str[:4].astype(int).between(start_year, end_year)]
    monthly_user_counts = filtered_df.groupby('MonthYear')['Downloads'].sum().reset_index()
    print("filter_df for downloads")
    print(monthly_user_counts)
    monthly_user_counts['MonthYear'] = monthly_user_counts['MonthYear'].astype(str)
    return monthly_user_counts.to_json(orient='records')


@app.route('/api/upload')
def get_monthly_uploads():

    year_range = request.args.getlist('year_range')  # Get the year range from the request query parameters as a list
    if len(year_range) != 2:
        return "Invalid year range", 400  # Return a 400 Bad Request if the year range is invalid

    # Parse the year range strings into integers
    start_year = int(year_range[0])
    end_year = int(year_range[1])

    # Filter data based on the year range
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['MonthYear'] = df['Timestamp'].dt.to_period('M')
    df['MonthYear'] = df['MonthYear'].astype(str)
    filtered_df = df[df['MonthYear'].str[:4].astype(int).between(start_year, end_year)]
    monthly_user_counts = filtered_df.groupby('MonthYear')['Upload'].nunique().reset_index()
    monthly_user_counts['MonthYear'] = monthly_user_counts['MonthYear'].astype(str)
    return monthly_user_counts.to_json(orient='records')


@app.route('/api/verify')
def get_monthly_verify():

    year_range = request.args.getlist('year_range')  # Get the year range from the request query parameters as a list
    if len(year_range) != 2:
        return "Invalid year range", 400  # Return a 400 Bad Request if the year range is invalid

    # Parse the year range strings into integers
    start_year = int(year_range[0])
    end_year = int(year_range[1])

    # Filter data based on the year range
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['MonthYear'] = df['Timestamp'].dt.to_period('M')
    df['MonthYear'] = df['MonthYear'].astype(str)
    filtered_df = df[df['MonthYear'].str[:4].astype(int).between(start_year, end_year)]
    monthly_user_counts = filtered_df.groupby('MonthYear')['Verify'].nunique().reset_index()
    monthly_user_counts['MonthYear'] = monthly_user_counts['MonthYear'].astype(str)
    return monthly_user_counts.to_json(orient='records')













# Route for serving data for Verify graph
# Route for serving data for Verify graph
@app.route('/api/verify_graph_data')
def get_verify_graph_data():
    year_range = request.args.getlist('year_range')  # Get the year range from the request query parameters as a list
    if len(year_range) != 2:
        return "Invalid year range", 400  # Return a 400 Bad Request if the year range is invalid

    # Parse the year range strings into integers
    start_year = int(year_range[0])
    end_year = int(year_range[1])

    # Filter data based on the year range
    df['MonthYear'] = df['MonthYear'].astype(str)
    filtered_df = df[df['MonthYear'].str[:4].astype(int).between(start_year, end_year)]
    # print(filtered_df)
    verify_graph_data = filtered_df.groupby(['Username', 'Project'])['Verify'].sum().reset_index()
    return verify_graph_data.to_json(orient='records')



# Route for serving data for activity type pie chart
@app.route('/api/activity_type_distribution')
def get_activity_type_distribution():
    year_range = request.args.getlist('year_range')  # Get the year range from the request query parameters as a list
    if len(year_range) != 2:
        return "Invalid year range", 400  # Return a 400 Bad Request if the year range is invalid

    # Parse the year range strings into integers
    start_year = int(year_range[0])
    end_year = int(year_range[1])

    # Filter data based on the year range
    df['MonthYear'] = df['MonthYear'].astype(str)
    filtered_df = df[df['MonthYear'].str[:4].astype(int).between(start_year, end_year)]
    # print("filtered_df activity pie ")
    # print(filtered_df)
    activity_type_distribution = filtered_df['Activity_Type'].value_counts().reset_index().rename(columns={'index': 'Activity_Type', 'Activity_Type': 'Count'})
    return activity_type_distribution.to_json(orient='records')


# Route for serving data for department pie chart
# Route for serving data for department pie chart
@app.route('/api/department_distribution')
def get_department_distribution():
    year_range = request.args.getlist('year_range')  # Get the year range from the request query parameters as a list
    if len(year_range) != 2:
        return "Invalid year range", 400  # Return a 400 Bad Request if the year range is invalid

    # Parse the year range strings into integers
    start_year = int(year_range[0])
    end_year = int(year_range[1])

    # Filter data based on the year range
    df['MonthYear'] = df['MonthYear'].astype(str)
    filtered_df = df[df['MonthYear'].str[:4].astype(int).between(start_year, end_year)]
    # print(filtered_df)
    department_distribution = filtered_df['Department'].value_counts().reset_index().rename(columns={'index': 'Department', 'Department': 'Count'})
    return department_distribution.to_json(orient='records')


# Route for serving data for download device pie chart
@app.route('/api/download_device_distribution')
def get_download_device_distribution():
    # Assuming df is your DataFrame containing the data
    year_range = request.args.getlist('year_range')  # Get the year range from the request query parameters as a list
    if len(year_range) != 2:
        return "Invalid year range", 400  # Return a 400 Bad Request if the year range is invalid

    # Parse the year range strings into integers
    start_year = int(year_range[0])
    end_year = int(year_range[1])

    # Filter data based on the year range
    df['MonthYear'] = df['MonthYear'].astype(str)
    filtered_df = df[df['MonthYear'].str[:4].astype(int).between(start_year, end_year)]
    # print(filtered_df)
    download_device_distribution = filtered_df['Download_Device_Type'].value_counts().reset_index().rename(columns={'index': 'Download_Device_Type', 'Download_Device_Type': 'Count'})
    return download_device_distribution.to_json(orient='records')

@app.route('/api/city_user_counts')
def get_city_user_counts():
    # Assuming you have city_user_counts DataFrame available
    # Convert DataFrame to JSON format and return
    # Aggregate the count of distinct users for each city
    city_user_counts = df.groupby('City')['Username'].nunique().reset_index()
    city_user_counts.columns = ['City', 'User Count']
    
    # Assuming you have latitude and longitude information in the same DataFrame
    # If latitude and longitude are available in the same DataFrame
    city_lat_lon = df.groupby('City').agg({'Latitude': 'mean', 'Longitude': 'mean'}).reset_index()
    
    # Merge city_user_counts with city_lat_lon to get latitude and longitude for each city
    city_user_counts = city_user_counts.merge(city_lat_lon, on='City', how='left')

    return city_user_counts.to_json(orient='records')

@app.route('/api/project_type_data')
def project_type_data():
    projects_per_type = df['Project'].value_counts()
    return projects_per_type.to_json(orient='records')



    
if __name__ == '__main__':
    app.run(debug=True)
