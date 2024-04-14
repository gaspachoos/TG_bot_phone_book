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

@bot.callback_query_handler(func=lambda callback: callback.data == 'open')
def open_menu(callback):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('Добавить контакт 🤝', callback_data='add')
    btn3 = types.InlineKeyboardButton('Просмотр контактов 👀', callback_data='show')
    markup.row(btn2, btn3)
    btn4 = types.InlineKeyboardButton('Поиск контакта 🔍', callback_data='find')
    btn5 = types.InlineKeyboardButton('Удалить контакт 🗑', callback_data='delete')
    markup.row(btn4, btn5)
    btn6 = types.InlineKeyboardButton('Изменить контакт 👥', callback_data='change')
    btn7 = types.InlineKeyboardButton('Выход из меню 🚶', callback_data='exit')
    markup.row(btn6, btn7)
    bot.send_message(callback.message.chat.id, '<b>Меню:</b>', reply_markup=markup,parse_mode='html')

@bot.callback_query_handler(func=lambda callback: callback.data == 'show')
def show_contacts(callback):
    try:
        with open('users.json', 'r') as file:
            contacts = json.load(file)
        response = "<b>Контакты:</b>\n"
        for contact in contacts:
            response += f"Имя: {contact.get('user name', 'Неизвестно')}, Телефон: {contact.get('user phone', 'Нет')}, Email: {contact.get('user email', 'Нет')} \n"
        bot.send_message(callback.message.chat.id, response, parse_mode='html')
    except (FileNotFoundError, json.JSONDecodeError):
        markup = types.InlineKeyboardMarkup()
        mmm = types.InlineKeyboardButton('Возврат в меню.', callback_data='open')
        markup.row(mmm)
        bot.send_message(callback.message.chat.id, "<b>Список контактов пуст:</b> 🥲", reply_markup=markup,parse_mode='html')