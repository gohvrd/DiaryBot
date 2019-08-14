import telebot

file = open('my.token')
token = file.readline()

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_and_help(message):
    user_id = message.from_user.id

    

    bot.send_message(message.from_user.id, "Системное меню start")

@bot.message_handler(commands=['help'])
def start_and_help(message):
    bot.send_message(message.from_user.id, "Системное меню help")

@bot.message_handler(content_types=['text'])
def start(message):
    global is_retry
    if is_retry:
        get_name(message)
        is_retry = False
        return

    if message.text == 'Привет':
        bot.send_message(message.from_user.id, "Привет!!! Я - бот-блокнот!")
    elif message.text == 'Давай знакомиться':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Предложи мне познакомиться: \"Давай знакомиться\"')

def get_name(message):
    global name
    name = message.text

    keyboard = telebot.types.InlineKeyboardMarkup()
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)

    bot.send_message(message.from_user.id, 'Значит тебя зовут ' + name + '?', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global is_retry

    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Очень приятно!')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Давай попробуем еще раз')
        is_retry = True

bot.polling(none_stop=True, interval=0)