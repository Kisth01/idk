import telebot
import webbrowser

bot = telebot.TeleBot("8394435730:AAFVPGyiim9szIGylUftelogEir29f27noA")

@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open("http://GitHub.com")


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}!")


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, "<b>Help</b> <em><u>information</u></em>", parse_mode='HTML')

@bot.message_handler()
def info(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}!")
    elif message.text.lower() == "id":
        bot.reply_to(message, message.from_user.id)

bot.polling(none_stop=True)
# bot.infinity_polling()