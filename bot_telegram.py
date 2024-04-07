import telebot
from telebot import types

TOKEN = ""

bot = telebot.TeleBot(TOKEN)

users_dict = {}
house = ('https://www.youtube.com/watch?v=Gp_JII49NCk&ab_channel=%D0%A8%D0%9A%D0%9E%D0%9B%D0%90%D0%A1%D0%A3%D0%A7%D0'
         '%90%D0%A1%D0%9D%D0%98%D0%A5%D0%A2%D0%90%D0%9D%D0%A6%D0%86%D0%92%E2%97%BE%EF%B8%8FONTOP%E2%97%BE%EF%B8%8F')


@bot.message_handler(commands=['start'])
def send_start_message(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()

    appointment_button = types.InlineKeyboardButton(text="Записаться на занятие 🕺",
                                                    callback_data=f"appointment_{chat_id}")
    about_iskra_button = types.InlineKeyboardButton(text="Почему Вы должны выбрать именно Искру? 💫",
                                                    callback_data=f"about_iskra_{chat_id}")

    keyboard.row(appointment_button)
    keyboard.row(about_iskra_button)

    bot.send_message(message.chat.id,
                     f"Привет, <b>{message.from_user.first_name}</b>! \n"
                     "Я бот танцевальной студии 'Искра' в Нижнем Новгороде.💥 \n"
                     "Впервые у нас? \n"
                     "Я помогу тебе записаться на первое занятие и подберу группу, исходя из твоего опыта и вкусов! \n",
                     parse_mode='html',
                     reply_markup=keyboard)


def save_fio(message):
    chat_id = message.chat.id
    fio = message.text
    if chat_id not in users_dict:
        users_dict[chat_id] = {}

    users_dict[chat_id]['ФИО'] = fio
    bot.send_message(chat_id,
                     f"Отлично, <b>{fio}</b>! Теперь, пожалуйста, введите ваш контактный телефон.",
                     parse_mode='html')
    bot.register_next_step_handler(message, save_phone)


def save_experience(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    one_button = types.InlineKeyboardButton(text="<1 года",
                                            callback_data=f"one_{chat_id}")
    one_to_three_button = types.InlineKeyboardButton(text="от 1 до 3 лет",
                                                     callback_data=f"1_3_{chat_id}")
    more_than_three_button = types.InlineKeyboardButton(text=">3 лет",
                                                        callback_data=f"3_{chat_id}")
    never_button = types.InlineKeyboardButton(text="Не занимался/Не занималась танцами",
                                              callback_data=f"never_{chat_id}")
    keyboard.add(one_button, one_to_three_button, more_than_three_button, never_button)
    bot.send_message(chat_id,
                     f"Занимались ли Вы танцами раньше? Если да, то сколько?",
                     parse_mode='html',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, save_status)


def save_fio_child(message):
    chat_id = message.chat.id
    fio = message.text
    users_dict[chat_id]['ФИО_ребенка'] = fio
    bot.send_message(chat_id,
                     f"Отлично, записали <b>{fio}</b>!",
                     parse_mode='html')
    save_experience(message)


def save_phone(message):
    chat_id = message.chat.id
    phone = message.text
    users_dict[chat_id]['Номер'] = phone

    keyboard = types.InlineKeyboardMarkup()
    me_button = types.InlineKeyboardButton(text="Я хочу записаться сам на занятие🙎🏻‍♂️🙍🏼‍♀️",
                                           callback_data=f"me_{chat_id}")
    child_button = types.InlineKeyboardButton(text="Я хочу записать на занятие ребенка 👩‍👧👨‍👧",
                                              callback_data=f"child_{chat_id}")
    keyboard.row(me_button)
    keyboard.row(child_button)
    bot.send_message(chat_id,
                     f"Вы ввели <b>{phone}</b>.",
                     parse_mode='html')
    bot.send_message(chat_id,
                     "Ниже выберите одну из опций 🔽",
                     parse_mode='html',
                     reply_markup=keyboard)


def save_status(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton(text="ДА☑️",
                                            callback_data=f"yes_{chat_id}")
    no_button = types.InlineKeyboardButton(text="НЕТ➖",
                                           callback_data=f"no_{chat_id}")
    keyboard.add(yes_button, no_button)
    bot.send_message(chat_id,
                     "Последний вопрос. Вы записываетесь к нам на занятие впервые?",
                     parse_mode='html',
                     reply_markup=keyboard)


def recommend_group(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    group = ["Хип хоп с нуля 13+", 'Хаус', 'Krump', 'Вог']
    for name in group:
        keyboard.add(types.InlineKeyboardButton(text=name, callback_data=name))
    bot.send_message(chat_id,
                     "Вам подойдут следующие группы: \n"
                     "Выберите стиль, на который хотели бы записаться \n"
                     "Про каждый из стилей можно почитать вот тут\n"
                     f"<b>ХАУС</b> - {house} Этот танец привлекает уникальной манерой и динамикой исполнения. Современный "
                     "хаус – это"
                     "быстрые движения ног, напоминающие степ, чечетку, шаги сальсы и латины, в сочетании с "
                     "плавными, абсолютно расслабленными движениями корпусом и головой. \n",
                     parse_mode='html',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    if call.data.startswith('appointment_'):
        bot.send_message(chat_id,
                         "Пожалуйста, напишите ваши ФИО",
                         parse_mode='html')
        bot.answer_callback_query(call.id)
        bot.register_next_step_handler(call.message, save_fio)
    elif call.data.startswith('me_'):
        users_dict[chat_id]['Запись'] = "Я хочу записаться сам на занятие"
        bot.answer_callback_query(call.id)
        save_experience(call.message)
    elif call.data.startswith('child_'):
        users_dict[chat_id]['Запись'] = "Я хочу записать ребенка на занятие"
        bot.send_message(chat_id,
                         f"Отлично, теперь напишите ФИО вашего ребенка!",
                         parse_mode='html')
        bot.answer_callback_query(call.id)
        bot.register_next_step_handler(call.message, save_fio_child)
    elif call.data.startswith('one_'):
        users_dict[chat_id]['Опыт'] = "меньше года"
        bot.answer_callback_query(call.id)
        save_status(call.message)
    elif call.data.startswith('1_3_'):
        users_dict[chat_id]['Опыт'] = "1-3 года"
        bot.answer_callback_query(call.id)
        save_status(call.message)
    elif call.data.startswith('3_'):
        users_dict[chat_id]['Опыт'] = "больше 3 лет"
        bot.answer_callback_query(call.id)
        save_status(call.message)
    elif call.data.startswith('never_'):
        users_dict[chat_id]['Опыт'] = "никогда"
        bot.answer_callback_query(call.id)
        save_status(call.message)
    elif call.data.startswith('yes_'):
        users_dict[chat_id]['Бывали у нас?'] = "ДА!"
        bot.answer_callback_query(call.id)
        recommend_group(call.message)
    elif call.data.startswith('no_'):
        users_dict[chat_id]['Бывали у нас?'] = "НЕТ("
        bot.answer_callback_query(call.id)
        recommend_group(call.message)


bot.polling()
