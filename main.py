import telebot
from config import token
from model import get_class

# Замени 'TOKEN' на токен твоего бота
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "HI! I am your Telegram bot. Use commands /hello, /bye, /start or upload some cloud pictures for me to analyze them")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Hi! How are you?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Bye!")

@bot.message_handler(content_types=['photo'])
def photo(message):
    #получаем файл и сохраняем
    file_info = bot.get_file(message.photo[-1].file_id) 
    file_name = file_info.file_path.split('/')[-1]
    #загружаем файл
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    #анализ изображения
    result = get_class(model_path="keras_model.h5", labels_path="labels.txt", image_path=file_name)
    bot.send_message(message.chat.id, result)

# Запускаем бота
bot.polling()
