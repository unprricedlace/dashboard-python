# Analytics Dashboard API

This repository contains a Flask application that provides a backend for an analytics dashboard. The application exposes several API endpoints that allow users to fetch data for visualizations such as graphs, pie charts, and bar charts based on user activities, project distributions, department statistics, and more.

## Features

- **Verify Graph Data**: Returns data for creating verification graphs based on user and project interactions.
- **Activity Type Distribution**: Provides a distribution of activity types over a specified year range.
- **Department Distribution**: Shows the distribution of activities across different departments.
- **Download Device Distribution**: Displays statistics on the types of devices used for downloads.
- **City User Counts**: Aggregates user counts by city including geographical coordinates for mapping.
- **Project Type Data**: Returns data for project distribution analysis.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.6 or higher
- Flask
- Pandas

You can install the necessary libraries using pip:

## Setup

To run this project, clone the repository and navigate to the project directory:

bash
git clone https://github.com/your-username/your-project-name.git
cd your-project-name
python app.py
curl http://127.0.0.1:5000/api/verify_graph_data?year_range=2018&year_range=2020

Feel free to adjust the `git clone` URL and any other specific details to suit your project's actual setup and requirements.
