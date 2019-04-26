import telegram

from telegram.ext import Updater, CommandHandler

def echo(bot, chat, mensagem):
    bot.sendMessage(chat_id=chat, text = mensagem)

bot = telegram.Bot(token = '625881619:AAFkDG8Fw8btJxVzWyz-GCru3nrT7gXYvfc')
echo(bot, '798821507', 'Ola Lucas, o que deseja fazer: \n 1 - Consultar eventos \n 2 - Editar eventos\n 3 - Apagar eventos\n 4 - Criar eventos')

# @botMensagem.message_handler(func=lambda m: True)

def start(update, context):
	print("RODOUUU RODADO IMPO")
	update.message.reply_text('Funciona')
	job = context.job
	context.bot.send_message(job.context, text='Beep!')

def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater('625881619:AAFkDG8Fw8btJxVzWyz-GCru3nrT7gXYvfc',user_sig_handler=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # dp.add_error_handler(error)

    updater.start_polling()
    print("RODOUUU RODADO")

    updater.idle()


# botMensagem.polling()

if __name__ == '__main__':
	main()
