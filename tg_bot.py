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


@bot.callback_query_handler(func=lambda callback: callback.data == 'find')
def find_contact(callback):
    try:
        with open('users.json', 'r') as file:
            contacts = json.load(file)
        if contacts:
            bot.send_message(callback.message.chat.id, "Введите элемент контакта:")
            bot.register_next_step_handler(callback.message, search_contacts)
        else:
            bot.send_message(callback.message.chat.id, "Контактов нет")
    except (FileNotFoundError, json.JSONDecodeError):
        markup = types.InlineKeyboardMarkup()
        mmm = types.InlineKeyboardButton('Возврат в меню.', callback_data='open')
        markup.row(mmm)
        bot.send_message(callback.message.chat.id, "<b>Список контактов пуст:</b> 🥲", reply_markup=markup,parse_mode='html')

def search_contacts(message):
    user_input = message.text
    try:
        with open('users.json', 'r') as file:
            contacts = json.load(file)
        found_contacts = []
        for contact in contacts:
            if user_input in contact.get('user name', '') or \
               user_input in contact.get('user phone', '') or \
               user_input in contact.get('user email', ''):
                found_contacts.append(contact)
        if found_contacts:
            response = "\n".join([f"Имя: {contact['user name']}, Телефон: {contact['user phone']},  Email: {contact['user email']}" for contact in found_contacts])
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton('Вернуться в меню', callback_data='open')
            markup.row(btn)
            bot.send_message(message.chat.id, response, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f"Контакт с '{user_input}' не найден")
    except (FileNotFoundError, json.JSONDecodeError):
        markup = types.InlineKeyboardMarkup()
        mmm = types.InlineKeyboardButton('Возврат в меню.', callback_data='open')
        markup.row(mmm)
        bot.send_message(message.chat.id, "<b>Произошла ошибка при чтении файла контактов:</b> 🥲", reply_markup=markup,parse_mode='html')        


@bot.callback_query_handler(func=lambda callback: callback.data == 'add')
def add_contact(callback):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("Да")
    btn2 = types.KeyboardButton("Нет")
    markup.add(btn1, btn2)
    bot.send_message(callback.message.chat.id, "Хотите добавить имя для данного контакта? 🧐", reply_markup=markup)
    bot.register_next_step_handler(callback.message, process_name_answer, {})

def process_name_answer(message, user_info):
    if message.text == "Да":
        bot.send_message(message.chat.id, "Введите имя для контакта:")
        bot.register_next_step_handler(message, process_phone_answer, user_info)
    elif message.text == "Нет":
        user_info["user name"] = "Пусто"
        process_phone_answer(message, user_info)
    else:
        markup = types.InlineKeyboardMarkup()
        ttt = types.InlineKeyboardButton('Возврат в меню. Попробуйте заного! 😤', callback_data='open')
        markup.row(ttt)
        bot.send_message(message.chat.id, '<b>Ошибка ввода 🤌</b>', reply_markup=markup,parse_mode='html')
        bot.register_next_step_handler(message, process_name_answer, user_info)

def process_phone_answer(message, user_info):
    if message.text != "Нет":
        user_info["user name"] = message.text
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("Да")
    btn2 = types.KeyboardButton("Нет")
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, "Хотите добавить номер телефона для данного контакта? 🧐", reply_markup=markup)
    bot.register_next_step_handler(message, process_phone_input, user_info)

def process_phone_input(message, user_info):
    if message.text == "Да":
        user_info["user phone"] = []
        bot.send_message(message.chat.id, "Введите номер телефона для контакта:")
        bot.register_next_step_handler(message, process_phone_save, user_info)
    elif message.text == "Нет":
        user_info["user phone"] = "Пусто"
        process_email_answer(message, user_info)
    else:
        markup = types.InlineKeyboardMarkup()
        jjj = types.InlineKeyboardButton('Возврат в меню. Попробуйте заного! 😤', callback_data='open')
        markup.row(jjj)
        bot.send_message(message.chat.id, '<b>Ошибка ввода 🤌</b>', reply_markup=markup,parse_mode='html')        
        bot.register_next_step_handler(message, process_phone_input, user_info)

def process_phone_save(message, user_info):
    user_info["user phone"].append(message.text)
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("Да")
    btn2 = types.KeyboardButton("Нет")
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, "Хотите добавить еще один номер телефона для данного контакта? 🧐", reply_markup=markup)
    bot.register_next_step_handler(message, process_additional_phone, user_info)

def process_additional_phone(message, user_info):
    if message.text == "Да":
        bot.send_message(message.chat.id, "Введите дополнительный номер телефона для контакта:")
        bot.register_next_step_handler(message, process_phone_save, user_info)
    elif message.text == "Нет":
        process_email_answer(message, user_info)
    else:
        markup = types.InlineKeyboardMarkup()
        vvv = types.InlineKeyboardButton('Возврат в меню. Попробуйте заного! 😤', callback_data='open')
        markup.row(vvv)
        bot.send_message(message.chat.id, '<b>Ошибка ввода 🤌</b>', reply_markup=markup,parse_mode='html')
        bot.register_next_step_handler(message, process_additional_phone, user_info)

def process_email_answer(message, user_info):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("Да")
    btn2 = types.KeyboardButton("Нет")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Хотите добавить email для данного контакта? 🧐", reply_markup=markup)
    bot.register_next_step_handler(message, process_email_save, user_info)

def process_email_save(message, user_info):
    if message.text == "Да":
        bot.send_message(message.chat.id, "Введите email для контакта:")
        bot.register_next_step_handler(message, save_contact, user_info)
    elif message.text == "Нет":
        user_info["user email"] = "Пусто"
        save_contact(message, user_info)
    else:
        markup = types.InlineKeyboardMarkup()
        zzz = types.InlineKeyboardButton('Возврат в меню. Попробуйте заного! 😤', callback_data='open')
        markup.row(zzz)
        bot.send_message(message.chat.id, '<b>Ошибка ввода 🤌</b>', reply_markup=markup,parse_mode='html')   
        bot.register_next_step_handler(message, process_email_save, user_info)

def save_contact(message, user_info):
    if message.text != "Нет":
        user_info["user email"] = message.text
    try:
        with open("users.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError,json.JSONDecodeError):
        data = []
    data.append(user_info)
    with open("users.json", "w") as file:
        json.dump(data, file, indent=4,ensure_ascii=False)
    markup = types.InlineKeyboardMarkup()
    mmm = types.InlineKeyboardButton('Возврат в меню.', callback_data='open')
    markup.row(mmm)
    bot.send_message(message.chat.id, '<b>Контакт сохранен ✍️.</b>', reply_markup=markup,parse_mode='html')


@bot.callback_query_handler(func=lambda callback: callback.data == 'delete')
def porcces_delete_user(callback):
    try:
        with open('users.json', 'r', encoding='utf-8') as file:
                contacts = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        contacts = [] 
    if not contacts:
        markup = types.InlineKeyboardMarkup()
        mmm = types.InlineKeyboardButton('Возврат в меню.', callback_data='open')
        markup.row(mmm)
        bot.send_message(callback.message.chat.id, '<b>Список контактов пуст: 🥲</b>', reply_markup=markup,parse_mode='html')
    else:    
        bot.send_message(callback.message.chat.id, "Введите имя контакта для удаления:🧐 ")
        bot.register_next_step_handler(callback.message, delete_contact)

def delete_contact(message):
    search_query = message.text.lower()
    try:
        with open('users.json', 'r', encoding='utf-8') as file:
            contacts = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        contacts = []
    
    found_contacts = []
    indexes_to_modify = []
    for i, contact in enumerate(contacts):
        if search_query in str(contact.get('user name', '')).lower():
            found_contacts.append(contact)
            indexes_to_modify.append(i)
    
    if found_contacts:
        for i, contact in enumerate(found_contacts, 1):
            bot.send_message(message.chat.id, f"{i}. {contact}")

        bot.send_message(message.chat.id, "Введите номер контакта для удаления:🧐")
        bot.register_next_step_handler(message, lambda m: delete_selected_contact(m, indexes_to_modify, contacts))
    else:
        markup = types.InlineKeyboardMarkup()
        mmm = types.InlineKeyboardButton('Возврат в меню.', callback_data='open')
        markup.row(mmm)
        bot.send_message(message.chat.id, '<b>Контакт не найден.🧐</b>', reply_markup=markup,parse_mode='html')
        
def delete_selected_contact(message, indexes_to_modify, contacts):
    try:
        index = int(message.text) - 1
        if index in range(len(indexes_to_modify)):
            del contacts[indexes_to_modify[index]]
            with open('users.json', 'w', encoding='utf-8') as file:
                json.dump(contacts, file, ensure_ascii=False, indent=4)
                
            markup = types.InlineKeyboardMarkup()
            mmm = types.InlineKeyboardButton('Возврат в меню.', callback_data='open')
            markup.row(mmm)
            bot.send_message(message.chat.id, '<b>Контакт успешно удален.⚰️</b>', reply_markup=markup,parse_mode='html')
        else:      
            markup = types.InlineKeyboardMarkup()
            mmm = types.InlineKeyboardButton('Возврат в меню.', callback_data='open')
            markup.row(mmm)
            bot.send_message(message.chat.id, '<b>Некорректный номер контакта.😑</b>', reply_markup=markup,parse_mode='html')
    except ValueError:
        markup = types.InlineKeyboardMarkup()
        mmm = types.InlineKeyboardButton('Возврат в меню.', callback_data='open')
        markup.row(mmm)
        bot.send_message(message.chat.id, '<b>ведите корректный номер контакта.😑</b>', reply_markup=markup,parse_mode='html')

def load_contacts():
    try:
        with open('users.json', 'r', encoding='utf-8') as file:
            contacts = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        contacts = []
    return contacts