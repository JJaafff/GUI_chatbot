import streamlit as st
from difflib import SequenceMatcher
from datetime import datetime
import requests
from geopy.geocoders import Nominatim
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
import sys
import dotenv
import os

dotenv.load_dotenv()
API_KEY_LCT=os.getenv('API_KEY_LOC')
API_KEY_WEA=os.getenv('API_KEY_WTH')

geolocator = Nominatim(user_agent=API_KEY_LCT)

def get_lon_lat(city):
    location = geolocator.geocode(city)
    if location:
        return location.longitude, location.latitude
    else:
        return "City not found."

def get_weather(lon, lat):
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY_WEA}&units=metric'
        response = requests.get(url)
        response.raise_for_status()
        temperature = response.json()['main']['temp']
        return temperature
    except Exception:
        return "Weather data not available."


def rock_paper_scissors():
    class RockPaperScissors(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("ROCK PAPER SCISSORS")
            self.setGeometry(100, 100, 400, 200)
            self.label1 = QLabel("rock/paper/scissors:", self)
            self.label1.move(100, 15)
            self.input1 = QLineEdit(self)
            self.input1.setGeometry(200, 20, 150, 20)
            self.button1 = QPushButton("Play", self)
            self.button1.setGeometry(150, 60, 100, 30)
            self.button1.clicked.connect(self.computer_vs_human)
            self.result_label = QLabel("", self)
            self.result_label.setGeometry(20, 100, 350, 60)
            self.label2 = QLabel("Type quit to leave", self)
            self.label2.move(240, 35)


        def computer_vs_human(self):
            moves = ['rock', 'paper', 'scissors']
            player_move = self.input1.text().lower().strip()

            if player_move not in moves:
                self.result_label.setText(f"'{player_move}' is not a valid move.")
                return
            computer_move = random.choice(moves)
            if player_move == computer_move:
                result = "It's a tie!"
            elif (
                    (player_move == 'rock' and computer_move == 'scissors') or
                    (player_move == 'scissors' and computer_move == 'paper') or
                    (player_move == 'paper' and computer_move == 'rock')
            ):
                result = "You won!"
            else:
                result = "You lost!"

            self.result_label.setText(
                f"Your move: {player_move}, Computer move: {computer_move}. {result}"
            )

    app = QApplication(sys.argv)
    window = RockPaperScissors()
    window.show()
    app.exec_()

predefined_inputs_to_responses = {
    "Hi": "Hello, How are you doing today?",
    "What's your name": "I'm J'Jarvis, your virtual friend.",
    "How old are you": "I'm ageless, but I was coded quite recently.",
    "What can you do": "I can chat with you and tell the time or weather!",
    "tell me the time": "GET_TIME",
    "Who created you": "A Python programmer, Giorgi Jafaridze.",
    "Goodbye": "See you later! Take care.",
    "Thank you": "You're welcome!",
    "What's the weather in city": "GET WEATHER IN A CITY",
    "Tell me about Giorgi Jafaridze": "He is one of the greatest men who ever walked on this planet(earth)",
    "What do i wear in city": "WHAT DO I WEAR",
    "2+2": "Oh math",
    "Let's play rock, paper, scissors": "ROCK PAPER SCISSORS"
}

st.title("🤖 J'Jarvis")
st.subheader("Ask me something!")

def find_city(city_input):
    cities = [
        "Tbilisi","Poti","Batumi","Kutaisi","Rustavi","Zugdidi",
        "New York", "London", "Tokyo", "Paris", "Shanghai",
        "Dubai", "Singapore", "Los Angeles", "Barcelona", "Rome",
        "Istanbul", "Bangkok", "Hong Kong", "Chicago", "Toronto",
        "Sydney", "Berlin", "Amsterdam", "San Francisco", "Moscow",
        "Mexico City", "Mumbai", "São Paulo", "Seoul", "Beijing",
        "Madrid", "Lisbon", "Vienna", "Dublin", "Copenhagen",
        "Prague", "Budapest", "Warsaw", "Brussels", "Stockholm",
        "Helsinki", "Oslo", "Athens", "Cairo", "Cape Town",
        "Buenos Aires", "Rio de Janeiro", "Lima", "Jakarta", "Delhi",
        "Kuala Lumpur", "Manila", "Casablanca", "Tel Aviv", "Doha"

    ]

    for city in cities:
        if city.lower() in city_input:
            return city


if 'chat' not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("You:", placeholder="Type your question here").capitalize()
if user_input:
    best_match_response = "Sorry, I did not understand that question."
    best_match_score = 0.0

    for known_input in predefined_inputs_to_responses:
        similarity_score = SequenceMatcher(a=user_input.strip().lower(), b=known_input.lower()).ratio()
        if similarity_score > best_match_score:
            best_match_score = similarity_score
            best_match_response = predefined_inputs_to_responses[known_input]

    if best_match_response == "GET_TIME":
        best_match_response = f"The current time is: {datetime.now():%H:%M}"

    elif best_match_response == "GET WEATHER IN A CITY":
        city_name = find_city(user_input)
        if not city_name:
            best_match_response = f"Sorry, We could not find the city named {city_name}"
        lon, lat = get_lon_lat(city_name)
        if isinstance(lon, str):
            best_match_response = f"Sorry, The coordinates for the city named {city_name} was not found"
        temperature = get_weather(lon, lat)
        best_match_response = f"The weather is {temperature}°C in {city_name}."

    elif best_match_response == 'WHAT DO I WEAR':
        city_name = find_city(user_input)
        lon, lat = get_lon_lat(city_name)
        if isinstance(lon, str):
            best_match_response = f"Sorry, The city named {city_name} was not found"
        temperature = get_weather(lon, lat)
        if temperature > 22:
            best_match_response = f"It is very hot there, maybe it would be great to wear Shorts and Short-sleeved T-shirt."
        elif 10 < temperature < 22:
            best_match_response = f"It feels cool there, maybe it would be great to wear Hoodie and trousers(Jeans or smth)."
        else:
            best_match_response = f"It is very cold there, maybe it would be great to wear warmly, i would recommend Jacket and warm pants."

    elif best_match_response == 'Oh math':
        try:
            result = eval(user_input, {"__builtins__": None}, {})
            best_match_response = f"The answer is {result}"
        except Exception:
            best_match_response = "Sorry, I couldn't compute that."

    elif best_match_response == 'ROCK PAPER SCISSORS':
        rock_paper_scissors()
        best_match_response = 'It was great to play with you'

    print(f"J'Jarvis: {best_match_response}")

    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("J'Jarvis", best_match_response))

for speaker, message in st.session_state.chat:
    st.markdown(f"**{speaker}:** {message}")