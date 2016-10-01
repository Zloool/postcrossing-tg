import logging

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, Job)

from pcconnector import PostCardUser

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level=logging.INFO)
logger = logging.getLogger(__name__)
REGISTER, GETMAIL, GETPASSWORD = range(3)

pclogin = ''
pcpass = ''
listnumber = ''
users = dict()
updater = Updater(token='YOURTOKENGOESHERE')
jobqueue = updater.job_queue

def pccheck(bot, job):
    global listnumber
    pc = PostCardUser(pclogin, pcpass)
    number = pc.loginToPC()
    if(listnumber != number):
        bot.sendMessage(job.context, text='You have currently ' + number + ' unsed mails!')
        listnumber = number
    else:
        bot.sendMessage(job.context, text='w8 m8')

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hi! I am bot, made for checking your PostCrossing account! Type /register to begin") #TODO perepisat
    return REGISTER

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

#def echo(bot, update):
#    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)


def register(bot, update):
    user = update.message.from_user
#    logger.info("Bio of %s: %s" % (user.first_name, update.message.text))
    update.message.reply_text('Lets start! Give me your postcrossing.com email, please:')

    return GETMAIL

def getmail(bot, update):
    global pclogin
    user = update.message.from_user
#    logger.info("Bio of %s: %s" % (user.first_name, update.message.text))
    pclogin = update.message.text
    update.message.reply_text('Okay, now give me your passwod(yep, thats tottaly insecure):')

    return GETPASSWORD

def getpassword(bot, update):
    global pcpass
    global listnumber
    user = update.message.from_user
#    logger.info("Bio of %s: %s" % (user.first_name, update.message.text))
    pcpass = update.message.text
    update.message.reply_text('All done! Now i will check your ackount')

    pc = PostCardUser(pclogin, pcpass)
    number = pc.loginToPC()
    update.message.reply_text('You have currently ' + number + ' unsed mails!')

    listnumber = number
    chat_id = update.message.chat_id
    second_checker = Job(pccheck, 1.0, context=chat_id)
    jobqueue.put(second_checker, next_t=0.0)
    return ConversationHandler.END



def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def main():

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            REGISTER: [CommandHandler('register', register)],
            GETMAIL: [RegexHandler('^.*$', getmail)],
            GETPASSWORD: [RegexHandler('^.*$', getpassword)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
