import telebot
from dotenv import load_dotenv
load_dotenv()
import os
import requests
from flask import Flask, request

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEATHER_API = os.environ.get("WEATHER_API")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bizning ilk botimizga xush keldingiz!")


def get_weather(city):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric"
    response = requests.get(url)
    data = response.json()  
    print(data)

    if data.get("cod") != 200:  
        return "Shahar topilmadi!"
    
    temp = data["main"]["temp"]
    weather = data["weather"][0]["main"]
    description = data["weather"][0]["description"]
    shahar = data["name"]
    harorat = data ["main"]["feels_like"]
    # if data.get("weather") else "Unknown"


    return f"{city} shahridagi ob-havo: {weather} ({description}), harorat: {temp}°C"
    #return f"{shahar} shahridagi ob-havo: {weather} ({description}), harorat: {temp}°C, his qilinadigan harorat: {harorat}°C"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    city = message.text 
    weather_info = get_weather(city)
    bot.send_message(message.chat.id, weather_info)
    
@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():  
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://bot-1oxe.onrender.com/webhook')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))