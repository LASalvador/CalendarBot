from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
from googleCalendar import selecionarUmEvento, criaEvento, alterarEvento, deletarEvento

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

MAPEAR_ACAO, CRIAR, CONSULTAR, ALTERAR, DELETAR, CANCELAR = range(6)


def start(bot, update):
    reply_keyboard = [['Criar', 'Consultar','Alterar', 'Deletar']]

    update.message.reply_text(
        'Olá! Eu sou o Schedule Bot.Vim ajudar-te a controlar sua agenda.\n\n'
        'O que deseja fazer',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return MAPEAR_ACAO


def acao(bot, update):
    # user = update.message.from_user
    # logger.info("Gender of %s: %s", user.first_name, update.message.text)
    # update.message.reply_text('I see! Please send me a photo of yourself, '
    #                           'so I know what you look like, or send /skip if you don\'t want to.',
    #                           reply_markup=ReplyKeyboardRemove())
    acao = update.message.text

    if(acao == 'Criar'):
        update.message.reply_text('Digite as informações do evento que deseja criar no formato:\n' 
                                  'nome, ano , mês , dia, horaInicio, minutosInicio, horaFinal, MinutoFinal'  ,
                               reply_markup=ReplyKeyboardRemove())
        return CRIAR
    elif (acao == 'Consultar'):
        update.message.reply_text('Digite o nome do evento que deseja consultar',
                               reply_markup=ReplyKeyboardRemove())
        return CONSULTAR
    elif (acao == 'Alterar'):
        update.message.reply_text('Digite as informações do evento que deseja alterar',
                               reply_markup=ReplyKeyboardRemove())
        return ALTERAR
    elif (acao == 'Deletar'):
        update.message.reply_text('Digite o nome do evento que deseja deletar',
                               reply_markup=ReplyKeyboardRemove())
        return DELETAR

    return CANCELAR



def criar(bot, update):
    user = update.message.from_user
    logger.info("Criar %s: %s", user.first_name, update.message.text)
    evento = update.message.text
    evento = evento.split(',')

    link = criaEvento(evento[0],int(evento[1]),int(evento[2]),int(evento[3]),int(evento[4]),int(evento[5]),int(evento[6]),int(evento[7]))
    update.message.reply_text(link)
    return ConversationHandler.END

def consultar(bot, update):
    user = update.message.from_user
    logger.info("Consultar %s: %s", user.first_name, update.message.text)
    event = selecionarUmEvento(update.message.text)
    update.message.reply_text(event)    

    return ConversationHandler.END

def alterar(bot, update):
    user = update.message.from_user
    logger.info("Criar %s: %s", user.first_name, update.message.text)
    update.message.reply_text('O usuário deseja alterar um evento.')

    return ConversationHandler.END

def deletar(bot, update):
    user = update.message.from_user
    logger.info("Criar %s: %s", user.first_name, update.message.text)
    deletarEvento(update.message.text)
    update.message.reply_text('Evento excluído')
    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Tchau! Espero ter ajudado.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END



def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("625881619:AAFkDG8Fw8btJxVzWyz-GCru3nrT7gXYvfc")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MAPEAR_ACAO: [RegexHandler('^(Criar|Consultar|Alterar|Deletar)$', acao)],

            CRIAR: [MessageHandler(Filters.text, criar),
                    CommandHandler('cancel', cancel)],

            CONSULTAR: [MessageHandler(Filters.text, consultar),
                    CommandHandler('cancel', cancel)],

            ALTERAR: [MessageHandler(Filters.text, alterar),
                    CommandHandler('cancel', cancel)],

            DELETAR: [MessageHandler(Filters.text, deletar),
                    CommandHandler('cancel', cancel)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    print("Bot rodando")
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()