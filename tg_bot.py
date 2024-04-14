import json
import telebot
from telebot import types


empty = True

API_TOKEN = '6969338848:AAEJI6ASfd633tWXQASWRfDmXSiSylDPrYg'
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start_tg_bot(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}, я являюсь имитацией <b>Телефонной книги</b> 🙂',parse_mode='html')
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Открыть 📖', callback_data='open')
    markup.row(btn1)
    bot.reply_to(message, 'Телефонная книга', reply_markup=markup)