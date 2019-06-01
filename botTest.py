from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

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

    return ACAO


def acao(bot, update):
    # user = update.message.from_user
    # logger.info("Gender of %s: %s", user.first_name, update.message.text)
    # update.message.reply_text('I see! Please send me a photo of yourself, '
    #                           'so I know what you look like, or send /skip if you don\'t want to.',
    #                           reply_markup=ReplyKeyboardRemove())
    acao = update.message.text

    if(acao == 'Criar'):
        update.message.reply_text('Digite as informações do evento que deseja criar',
                               reply_markup=ReplyKeyboardRemove())
        return CRIAR
    elif (acao == 'Consultar'):
        update.message.reply_text('Digite as informações do evento que deseja consultar',
                               reply_markup=ReplyKeyboardRemove())
        return CONSULTAR
    elif (acao == 'Alterar'):
        update.message.reply_text('Digite as informações do evento que deseja alterar',
                               reply_markup=ReplyKeyboardRemove())
        return ALTERAR
    elif (acao == 'Deletar'):
        update.message.reply_text('Digite as informações do evento que deseja deletar',
                               reply_markup=ReplyKeyboardRemove())
        return DELETAR

    return CANCELAR



def criar(bot, update):
    user = update.message.from_user
    logger.info("Criar %s: %s", user.first_name, update.message.text)
    update.message.reply_text('O usuário deseja criar um evento.')

    return ConversationHandler.END

def consultar(bot, update):
    user = update.message.from_user
    logger.info("Consultar %s: %s", user.first_name, update.message.text)
    update.message.reply_text('O usuário deseja consultar um evento.')

    return ConversationHandler.END

def alterar(bot, update):
    user = update.message.from_user
    logger.info("Criar %s: %s", user.first_name, update.message.text)
    update.message.reply_text('O usuário deseja alterar um evento.')

    return ConversationHandler.END

def deletar(bot, update):
    user = update.message.from_user
    logger.info("Criar %s: %s", user.first_name, update.message.text)
    update.message.reply_text('O usuário deseja deletar um evento.')

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


    MAPEAR_ACAO, CRIAR, CONSULTAR, ALTERAR, DELETAR, CANCELAR = range(6)
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

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()