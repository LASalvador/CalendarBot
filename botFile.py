# https://github.com/python-telegram-bot/python-telegram-bot/blob/2cde878d1e5e0bb552aaf41d5ab5df695ec4addb/examples/timerbot.py

from telegram.ext import Updater, CommandHandler
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level=logging.INFO)

logger = logging.getLogger(__name__)

def echo(bot, chat, mensagem):
    bot.sendMessage(chat_id=chat, text = mensagem)

bot = telegram.Bot(token = '625881619:AAFkDG8Fw8btJxVzWyz-GCru3nrT7gXYvfc')
echo(bot, '798821507', 'Ola Lucas, o que deseja fazer: \n 1 - Consultar eventos \n 2 - Editar eventos\n 3 - Apagar eventos\n 4 - Criar eventos')

# @botMensagem.message_handler(func=lambda m: True)
def start(bot, update):
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')



# botMensagem.polling()

if __name__ == '__main__':
	main()	
