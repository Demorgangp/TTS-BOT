import telegram
from telegram import *
from telegram.ext import *

TOKEN = 'YOUR TOKEN' # Your botfather Token
admins = [1389873554] # Your numeric id, You can get it from @useinfobot
bot = Bot(TOKEN)
SELECT_SUBJ, MESSAGE = 0, 1
# You can edit keyboards here:
keyboard = [['Free Talk', 'Subject 1', 'Subject 2'],
            ['Subject 3', 'Subject 4','Subject 5' ],
            ['Others']                            ]
raw_keyboard = []
for j in keyboard:
    for i in j:
        raw_keyboard.append(i)
select_subj = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
send_message_keyboard = ReplyKeyboardMarkup([['Send Message']], resize_keyboard=True, one_time_keyboard=True)

def mention_with_name(id, name):
    return f'<a href="tg://user?id={id}">{name}</a>'

def start(update: Update, context: CallbackContext):
    message = update.message
    message.reply_text('Hello. To contact us you can use /send_message or the button below.', reply_markup=send_message_keyboard)
    return ConversationHandler.END

def send_message_command(update: Update, context: CallbackContext):
    message = update.message
    message.reply_text('Well, now choose the subject of your message from the list:', reply_markup=select_subj)
    return SELECT_SUBJ

def select_subject(update: Update, context: CallbackContext):
    message = update.message
    if message.text not in raw_keyboard:
        message.reply_text('<b>Please select the subject from the provided list below:</b>', parse_mode='html', reply_markup=select_subj)
        return SELECT_SUBJ
    else:
        message.reply_text('ok welldone.\nnow send me your message: ', reply_markup=ReplyKeyboardRemove())
        context.user_data['subj'] = message.text
        return MESSAGE

def get_message(update: Update, context: CallbackContext):
    message = update.message
    for admin in admins:
        # TODO or send it to a group
        context.bot.send_message(admin, f'<b>Subject: {context.user_data["subj"]}</b>\nSender: <b>{mention_with_name(message.from_user.id, message.from_user.full_name)}</b>\n\n{message.text}', parse_mode='html')
    message.reply_text('Thanks for your message. you can still use /send_message to contact us.', reply_markup=send_message_keyboard)
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Canceled')
    return ConversationHandler.END


def main():
    import pytz
    updater = Updater(TOKEN, defaults=Defaults(tzinfo=pytz.timezone('Asia/Tehran') ))
    # dp = updater.dispatcher
    dp = Dispatcher(bot, None, workers=0, use_context=True)

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^Send Message'), send_message_command), CommandHandler('send_message', send_message_command)],
        states={
            SELECT_SUBJ: [CommandHandler('cancel', cancel), CommandHandler('start', start),
                          MessageHandler(Filters.text, select_subject)],
            MESSAGE: [CommandHandler('cancel', cancel), CommandHandler('start', start),
                      MessageHandler(Filters.all, get_message)],
        },
        fallbacks=[CommandHandler('start', start)],
    ))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

