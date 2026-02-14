import telebot
import requests
import json
bot = telebot.TeleBot('8394435730:AAFVPGyiim9szIGylUftelogEir29f27noA')
API = '3d9de74844d28377e81415151cbe6a66'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, напиши город')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city =  message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = res.json()
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']


        weather_desc = data['weather'][0]['description']
        weather_main = data['weather'][0]['main']

        wind_speed = data['wind']['speed']
        city_name = data['name']

        reply = (
            f"Погода в {city_name}:\n\n"
            f"Температура: {temperature:.1f}°C\n"
            f"Ощущается как: {feels_like:.1f}°C\n"
            f"Влажность: {humidity}%\n"
            f"Давление: {pressure} гПа\n"
            f"Ветер: {wind_speed} м/с\n"
            f"Состояние: {weather_desc}"
            )
        bot.reply_to(message, reply)
    else:
        bot.reply_to(message, 'Город указан не верно!')

bot.polling(True)