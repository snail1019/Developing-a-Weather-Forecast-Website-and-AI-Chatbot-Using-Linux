import os
from dotenv import load_dotenv
import requests
import streamlit as st
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Load the environment variables
load_dotenv("chatbot/.env")

API_KEY = "d94af54db46f43deb88151507240211"
BASE_URL = "http://api.weatherapi.com/v1"

def get_weather(city):
    url = f"{BASE_URL}/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["current"]["temp_c"]
        humidity = data["current"]["humidity"]
        date = data["location"]["localtime"]  
        return f"Weather in {city} on {date}: {temp}°C, Humidity: {humidity}%"
    else:
        return "Unable to retrieve weather data."

def get_forecast(city):
    url = f"{BASE_URL}/forecast.json?key={API_KEY}&q={city}&days=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast = data["forecast"]["forecastday"][0]
        date = forecast["date"]
        max_temp = forecast["day"]["maxtemp_c"]
        min_temp = forecast["day"]["mintemp_c"]
        condition = forecast["day"]["condition"]["text"]
        return f"Weather forecast for {city} on {date}: Max temperature: {max_temp}°C, Min temperature: {min_temp}°C, Condition: {condition}."
    else:
        return "Unable to retrieve weather forecast data."

def get_temperature(city):
    url = f"{BASE_URL}/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["current"]["temp_c"]
        return f"The current temperature in {city} is {temp}°C."
    else:
        return "Unable to retrieve temperature data."

def get_humidity(city):
    url = f"{BASE_URL}/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        humidity = data["current"]["humidity"]
        return f"The current humidity in {city} is {humidity}%."
    else:
        return "Unable to retrieve humidity data."

def get_yesterday_weather(city):
    url = f"{BASE_URL}/history.json?key={API_KEY}&q={city}&dt={get_yesterday_date()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        date = data["forecast"]["forecastday"][0]["date"]
        max_temp = data["forecast"]["forecastday"][0]["day"]["maxtemp_c"]
        min_temp = data["forecast"]["forecastday"][0]["day"]["mintemp_c"]
        condition = data["forecast"]["forecastday"][0]["day"]["condition"]["text"]
        return f"Weather in {city} on {date}: Max temperature: {max_temp}°C, Min temperature: {min_temp}°C, Condition: {condition}."
    else:
        return "Unable to retrieve yesterday's weather data."

def check_rain(city):
    url = f"{BASE_URL}/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        condition = data["current"]["condition"]["text"]
        if "rain" in condition.lower() or "shower" in condition.lower():
            return f"There is a chance of rain in {city}."
        else:
            return f"The weather in {city} is clear of rain."
    else:
        return "Unable to check rain condition."

def get_yesterday_date():
    from datetime import datetime, timedelta
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


st.set_page_config(
    page_title="AI Weather",
    page_icon="🌦️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center;'>🌦️ WEATHER FORECAST</h1>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if len(st.session_state.chat_history) == 0:  # Only ask once at the beginning of the conversation
    st.chat_message("assistant").markdown("How are you today? How can I assist you?")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask AI...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if "current weather" and "current weather"in user_input.lower():
        city = user_input.split("in")[-1].strip()
        assistant_response = get_weather(city) 
    elif "weather forecast" in user_input.lower() or "forecast" in user_input.lower():
        parts = user_input.lower().split("in")
        if len(parts) > 1:
            location = parts[1].strip() 
            if "on" in location:
                location_parts = location.split("on")
                city = location_parts[0].strip()  
                date = location_parts[1].strip()  
                # Get forecast based on city and date
                assistant_response = get_forecast(city)  
                # Update the response to include the specific date requested
                assistant_response = f"Weather forecast for {city} on {date}: " + assistant_response.split(": ", 1)[1]
            else:
                city = location
                assistant_response = get_forecast(city)  
        else:
            assistant_response = "Please provide a location."

    elif "temperature" in user_input.lower() or "temp" in user_input.lower():
        parts = user_input.lower().split("in")
        if len(parts) > 1:
            city = parts[1].strip()  
            assistant_response = get_temperature(city)  
        else:
            assistant_response = "Please specify a location."

    elif "humidity" in user_input.lower():
        parts = user_input.lower().split("in")
        if len(parts) > 1:
            city = parts[1].strip()  
            assistant_response = get_humidity(city) 
        else:
            assistant_response = "Please specify a location."

    elif any(keyword in user_input.lower() for keyword in ["yesterday's weather", "yesterday weather", "yesterday weather in"]):
        parts = user_input.lower().split("in")
        if len(parts) > 1:
            city = parts[1].strip() 
            assistant_response = get_yesterday_weather(city)  
        else:
            assistant_response = "Please specify a location."

    elif "is it raining" in user_input.lower():
        city = user_input.split("in")[-1].strip()
        assistant_response = check_rain(city)  
    else:
        assistant_response = "Sorry, I don't understand your request." 
        
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
