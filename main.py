from bot import Bot
import config

bot = Bot(config.TOKEN)


@bot.outgoing_message_handler(commands=["test"])
def get_msg(message):
    message.delete()
    bot.me.send_message(config.MY_ID, "test!!!")


bot.polling()
