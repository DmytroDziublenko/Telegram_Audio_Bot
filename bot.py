try:
    import telebot
    from os import remove
    from pytube import YouTube
    from django.core.validators import URLValidator
    from django.core.exceptions import ValidationError
except Exception as importE:
    print("Some Modules are Missing {}".format(importE))

TOKEN = 'TOKEN'

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
        print('done')
        path = 'audios/{}.mp4'.format(download_audio(message.text, 'audios/'))
        audio = open(path, 'rb')
        print('done')
        bot.send_audio(message.chat.id, audio)
        print('done')
        audio.close()
        print('done')
        remove(path)
        print('done')
    except ValidationError as validationE:
        bot.send_message(message.chat.id, "This is not a <b>url</b>!\nTry again)", parse_mode='html')
    else:
        audio.close()
        remove(path)


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
