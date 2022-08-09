import requests
import telebot
import time

with open("token", "r") as f:
    token = f.readline().rstrip()
    api_key = f.readline().rstrip()

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMUYrTgFRRVd6t1x2ChENkaYaDKXwYAAi4AAyRxYhqI6DZDakBDFCkE')
    bot.send_chat_action(message.from_user.id, 'typing')
    time.sleep(1)

    bot.send_message(message.from_user.id, 'Привет, {} ✋'.format(message.from_user.first_name))
    bot.send_chat_action(message.from_user.id, 'typing')
    time.sleep(1)
    bot.send_message(message.from_user.id, 'Напиши название города, в котором хочешь узнать текущую погоду 🌄')


@bot.message_handler(content_types=["text"])
def text(message):
    q = message.text
    params = {
        'q': q,
        'lang': "ru",
        'appid': api_key,
        'units': 'metric'
    }
    res = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
    if res.status_code == 200:
        res = res.json()
        print(res)
        bot.send_chat_action(message.from_user.id, 'typing')
        bot.send_message(message.from_user.id, "🏙 Город: ***{}***\n"
                                               "Ширина: {}°, долгота: {}°\n"
                                               "🌡 Температура: ***{}***°C\n"
                                               "Максимальная: {}°C, минимальная: {}°C\n"
                                               "Ощущается как: {}°C\n"
                                               "💨 Ветер: {}м/с\n"
                                               "📝 Состояние: ***{}***\n".format(res["name"],
                                                                                 res["coord"]["lat"],
                                                                                 res["coord"]["lon"],
                                                                                 res["main"]["temp"],
                                                                                 res["main"]["temp_max"],
                                                                                 res["main"]["temp_min"],
                                                                                 res["main"]["feels_like"],
                                                                                 res["wind"]["speed"],
                                                                                 res["weather"][0]["description"]),
                         parse_mode="Markdown")
    else:
        bot.reply_to(message, 'Неверное название города ❌ \nПовторите попытку ❗')


bot.polling()
