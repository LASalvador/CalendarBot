import telegram
import telebot

botMensagem = telebot.TeleBot('625881619:AAFkDG8Fw8btJxVzWyz-GCru3nrT7gXYvfc')

def echo(bot, chat, mensagem):
    bot.sendMessage(chat_id=chat, text = mensagem)

bot = telegram.Bot(token = '625881619:AAFkDG8Fw8btJxVzWyz-GCru3nrT7gXYvfc')
echo(bot, '798821507', 'Olá Lucas, o que deseja fazer: \n 1 - Consultar eventos \n 2 - Editar eventos\n 3 - Apagar eventos\n 4 - Criar eventos')

@botMensagem.message_handler(func=lambda m: True)

def escuta(message):
        if message.text == '1':
            echo(bot, '798821507', 'Nome do evento que deseja consultar:\n')
            
        elif message.text == '2':
            echo(bot, '798821507', 'Nome do evento que deseja editar:\n')
            
        elif message.text == '3':
            echo(bot, '798821507', 'Nome do evento que deseja apagar:\n')
            
        elif message.text == '4':
            echo(bot, '798821507', 'Nome do novo evento:\n')

def consulta(nomeEvento):

botMensagem.polling()
