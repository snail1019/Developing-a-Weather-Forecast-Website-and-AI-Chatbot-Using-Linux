# Developing-a-Weather-Forecast-Website-and-AI-Chatbot-Using-Linux
Project Overview

The goal of this project is to develop a weather forecast website using a Linux-based system. The website will utilize Bash shell scripting to process weather data retrieved from an API and display real-time weather information along with a 7-day forecast. Additionally, an AI-powered chatbot will be integrated to facilitate quick and efficient weather-related queries using English commands.

Main Idea

The project focuses on leveraging Linux shell scripting to automate data retrieval and processing. The core functionality revolves around extracting and displaying weather data from an external API. Users will input a city name, which will be used to construct an API request link, retrieve weather data, and ensure data accuracy before displaying it on a web interface using Flask.

Key Features

Main Functions:

Fetch weather data from an external API for real-time updates and a 7-day forecast.

Utilize Bash scripts to process retrieved JSON data and store it in structured files.

Display weather data using a web interface powered by Flask.

Additional Functions:

Implement an AI chatbot to facilitate interactive weather inquiries using English commands.

Create a city name library to prevent errors caused by incorrect input formats.

Encode and handle spaces in city names to ensure accurate API requests.

Project Workflow

The system workflow consists of multiple scripts working together to fetch, process, and display weather data:

app.py (Flask Web Application): Calls the check_api.sh script.

check_api.sh (API Data Retrieval):

Retrieves weather data from the API.

Stores current weather data in current_weather.json.

Stores 7-day forecast data in forecast_weather.json.

xulydulieu.sh (Data Processing):

Processes raw API data and filters relevant details.

Stores structured data in dataduocxuly.json.

Flask Web Interface:

Displays processed weather data from JSON files.

API Integration

To retrieve accurate weather data, the project will:

Utilize an external API such as weather.api.

Allow users to input a city name to generate the API request link dynamically.

Validate API data accuracy before processing.

Implement error handling for invalid inputs and ensure proper encoding of city names.

Expected Outcomes

By the end of the project, the system will be capable of:

Providing up-to-date weather forecasts for any specified location.

Ensuring efficient data processing through Bash shell scripting.

Offering an interactive and user-friendly web interface for weather updates.

Enhancing user experience with an AI chatbot for weather-related conversations.

This project combines Linux scripting, Flask web development, and API integration to deliver a functional and interactive weather forecasting website.


