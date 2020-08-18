try:
    import telebot
    from os import remove
    from time import sleep
    from pytube import YouTube
    from django.core.validators import URLValidator
    from requests.exceptions import ConnectionError
    from django.core.exceptions import ValidationError
except Exception as importE:
    print("Some Modules are Missing {}".format(importE))

TOKEN = '1092394684:AAHeE5z6yqHo7pAn36Sn_K4sAzaEvqgsl88'

bot = telebot.TeleBot(TOKEN)
validator = URLValidator()


@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('stickers/welcome.webp', 'rb')
    bot.send_message(message.chat.id,
                     "Welcome, {0.first_name}!\nI'm <b>{1.first_name}</b>\nSend me url on <b>YouTube</b> video "
                     "and I send you audio of this video".format(message.from_user, bot.get_me()),
                     parse_mode='html')
    bot.send_sticker(message.chat.id, sticker)
    sticker.close()


@bot.message_handler(content_types=['text'])
def send_audio(message):
    try:
        validator(message.text)
        path = 'audios/{}.mp4'.format(download_audio(message.text, 'audios/'))
        audio = open(path, 'rb')
        bot.send_audio(message.chat.id, audio)
        audio.close()
        remove(path)
        sleep(3)
    except ValidationError as validationE:
        bot.send_message(message.chat.id, "This is not a <b>url</b>!\nTry again)", parse_mode='html')
    except ConnectionError as connectionE:
        audio.close()
        remove(path)
        sleep(3)
        bot.send_message(message.chat.id, "Connection Error!\nTry again")


def download_audio(url, path):
    ytd = YouTube(url)
    title = remove_bad_symbols(ytd.title.title())
    ytd.streams.filter(only_audio=True).first().download(output_path=path, filename=title)
    return title


def remove_bad_symbols(st):
    i = 0
    tmp = ''
    while i < len(st):
        if st[i] == '\\' or st[i] == '/' or st[i] == '*' or st[i] == '?' or st[i] == '"' \
                or st[i] == '<' or st[i] == '>' or st[i] == '|' or st[i] == '#' or st[i] == '.':
            tmp += ' '
        else:
            tmp += st[i]
        i += 1
    return tmp


bot.polling(none_stop=True)
