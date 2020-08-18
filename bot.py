try:
    import telebot
except Exception as importE:
    print("Some Modules are Missing {}".format(importE))

TOKEN = 'TOKEN'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('stickers/welcome.webp', 'rb')
    bot.send_message(message.chat.id,
                     "Welcome, {0.first_name}!\nI'm <b>{1.first_name}</b>\nSend me url on <b>YouTube</b> video "
                     "and I send you audio of this video".format(message.from_user, bot.get_me()),
                     parse_mode='html')
    bot.send_sticker(message.chat.id, sticker)
    sticker.close()


bot.polling(none_stop=True)
