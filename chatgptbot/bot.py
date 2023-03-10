import telebot
import chatgptbot.copilot as cpl
import re
import time

bot = telebot.TeleBot('bot token')

@bot.message_handler(content_types=['text'])
def question(message):
    copilot = cpl.Copilot()
    a = copilot.get_answer(message.text)
    images_urls = []

    while len(images_urls) < 6:
        if 'alt text' in a:
            a = a.replace('![alt text](', '')
            a = a.replace('![alt text] (', '')
            a = a.replace(')', '')

        try:
            urls = re.search("(?P<url>https?://[^\s]+)", a).group("url")
        except AttributeError:
            break
        images_urls.append(urls)
        a = a.replace(urls, '')

    if a:
        bot.send_message(message.chat.id, a)

    for image_url in images_urls:
        time.sleep(0.2)
        try:
            bot.send_document(message.chat.id, image_url)
        except Exception as exp:
            bot.send_message(message.chat.id, f'Не удалось загрузить изображение\nВозможно, оно было удалено или перемещено')

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Привет ✋\nВ этом боте можно пообщаться с искуственным интелектом chatgpt 🖧')

