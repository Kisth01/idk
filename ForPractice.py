import telebot

bot = telebot.TeleBot('8394435730:AAFVPGyiim9szIGylUftelogEir29f27noA')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, message)

bot.polling(True)