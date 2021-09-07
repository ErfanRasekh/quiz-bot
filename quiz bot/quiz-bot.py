import logging
import telegram
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
import os
import mysql.connector
import time
import config

configs = config()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger(__name__)

FULLNAME, PHONENUMBER, DEGREE, LESSON, TIME, CONFIRMATION, SEND_MESSAGE, QUESTIONS, QUIZ, RESULTS, CHECKANSWER= range(11)

# connext to database
cnx = mysql.connector.connect(user='root', passwd = 'erfanerfan1320', db = 'questions')
cursor = cnx.cursor()

numberOfQuestion = 5

TOKEN = '1948746558:AAFC_i4bLRJvM9DPgJQaTuPqirfMEXHw6UU'
bot = telegram.Bot(token = TOKEN)
chat_id = '@azmouun_bo'
competitor_username = ''
PORT = int(os.environ.get('PORT', 80))

answerOfQuestion = 0
numberOfTrue = 0


def start(update, context):
    update.message.reply_text(
        "سلام،من ربات آزمون ساز هستم و میخوام بین شما و دوستت تو یه درس به انتخاب خودتون یه رقابت بندازم و همدیگه رو بسنجید \n \n پس بزن بریم")
    update.message.reply_text(
        "خب حالا دلم میخواد اسم و فامیلیت رو بنویسی اینجا تا با هم بیشتر آشنا شیم")

    return FULLNAME


def fullname(update, context):
    # give first name of user
    
    user = update.message.from_user
    user_data = context.user_data
    category = 'نام و نام خانوادگی'
    text = update.message.text
    user_data[category] = text

    logger.info("name of %s: %s", user.first_name, update.message.text)

    update.message.reply_text("حالا شماره موبایلتم بدی ممنون میشم")

    return PHONENUMBER


def phoneNumber(update, context):
    # give phone number of user

    user = update.message.from_user
    user_data = context.user_data
    category = 'شماره موبایل'
    text = update.message.text
    user_data[category] = text

    logger.info("phone number of %s: %s", user.first_name, update.message.text)

    update.message.reply_text("مقطع تحصیلیتو میشه انتخاب کنی؟", reply_markup= configs.degree_keys)
    
    return DEGREE


def degree(update, context):
    # give the degree of user

    user = update.message.from_user
    user_data = context.user_data
    category = 'مقطع تحصیلی'
    text = update.message.text
    user_data[category] = text

    logger.info("degree of %s: %s", user.first_name, update.message.text)
    
    update.message.reply_text('خب حالا این اطلاعاتتو تایید میکنی یا غلط زدیشو میخوای از اول تست کنیش؟؟؟ {}'.format(facts_to_str(user_data)), 
                            reply_markup= configs.confirmation_keys)

    return CONFIRMATION
    

def confirmation(update, context):
    user = update.message.from_user
    
    logger.info("confirmation of %s: %s", user.first_name, update.message.text)

    update.message.reply_text('خب حالا درسی که میخوای امتحان بدی با دوستت رو انتخاب کن', 
                            reply_markup= configs.lesson_keys)

    return LESSON


def lesson(update, context):
    # know the quiz subject

    user = update.message.from_user
    user_data = context.user_data
    category = 'درس مورد نظر'
    text = update.message.text
    user_data[category] = text

    logger.info("degree of %s: %s", user.first_name, update.message.text)

    update.message.reply_text("خب حالا آیدی تلگرام دوستتو بده ببینم آماده هست یا نه برا امتحان؟؟", 
                              reply_markup=ReplyKeyboardRemove())

    return SEND_MESSAGE


def send_message_to_channel(update, context):
    # send message to channel for anounce them

    user = update.message.from_user
    user_data = context.user_data
    category = 'رقیب'
    competitor_username = update.message.text
    user_data[category] = competitor_username
    user_data['امتیاز'] = 0
    first_username = update.message.chat.username
    logger.info("send message of %s: %s", user.first_name, update.message.text)

    bot.send_message(chat_id=chat_id,  text='<b> شما دو دوست دعوت به مبارزه شدید تو درس ' + user_data['درس مورد نظر'] + '.با زدن شروع روی آزمون،آزمون رو شروع کنید</b>  \n' +
                     "\n   @" + first_username + " VS @" + competitor_username,
                     parse_mode=telegram.ParseMode.HTML)

    update.message.reply_text(
        "میتونی بری تو کانال زیر و هر وقت دوستتم باشه میاد و با هم امتحان میدید دوست عزیز \n" + chat_id)
    update.message.reply_text(
        'Are you ready for the first question?', configs.quiz_keys)

    return QUIZ


def quiz(update, context):
    # start the quiz and handle it in dataOfQuestion

    dataOfQuestion(update, context)


def dataOfQuestion(update, context, id):
    # recive data from database and made the questions

    cursor.execute('SELECT * FROM physic')
    for result in cursor.fetchall():
        question = result[1]
        ans1 = result[2]
        ans2 = result[3]
        ans3 = result[4]
        ans4 = result[5]
        answerOfQuestion = result[6]
        mainQuestion = str(result[0]) + '-' + question + '  :\n1 - ' + ans1 + "\n2 - " + ans2 + '\n3 - ' + ans3 + '\n4 - ' + ans4
        update.message.reply_text(mainQuestion, reply_markup = configs.answer_keys)
        resultOfQuestion(update, context, answerOfQuestion)
        time.sleep(60)
    
    return resultOfQuestion


def resultOfQuestion(update, context, answerOfQuestion):
    # check the answer of user

    pass


def checkAnswer(update, context):
    # check the answer is true or false

    user_data = context.user_data

    number = user_data['امتیاز'] + 1
    user_data['امتیاز'] = number


def showResultOfQuiz(update, context):
    # end of quiz and show result of quiz in channel

    user = update.message.from_user
    user_data = context.user_data

    bot.send_message(chat_id=chat_id, text='<b>امتیاز و اطلاعات شما دو دوست عزیز</b>\n {}'.format(facts_to_str(user_data)))


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def cancel(update, context):
    pass


def facts_to_str(user_data):
    facts = list()
    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))  

    return "\n".join(facts).join(['\n', '\n'])


def main():
    updater = Updater(TOKEN, use_context = True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],

        states={
            FULLNAME:[CommandHandler('start', start), MessageHandler(Filters.text, fullname)],
            PHONENUMBER:[CommandHandler('start', start), MessageHandler(Filters.text, phoneNumber)],
            DEGREE:[CommandHandler('start', start), MessageHandler(Filters.text, degree)],
            CONFIRMATION:[CommandHandler('start', start), MessageHandler(Filters.regex('^مورد تایید است$'), confirmation), 
                          MessageHandler(Filters.regex('^شروع دوباره$'), start)],
            LESSON:[CommandHandler('start', start), MessageHandler(Filters.text, lesson)],
            TIME:[CommandHandler('start', start), MessageHandler(Filters.text, cancel)],
            SEND_MESSAGE:[CommandHandler('start', start), MessageHandler(Filters.text, send_message_to_channel)],
            QUESTIONS:[CommandHandler('start', start), MessageHandler(Filters.text, quiz)],
            QUIZ:[CommandHandler('start', start),MessageHandler(Filters.regex('^شروع$'), quiz)],
            RESULTS:[CommandHandler('start', start), MessageHandler(Filters.text, showResultOfQuiz)],
            CHECKANSWER:[CommandHandler('start', start), MessageHandler(Filters.text, checkAnswer)]
        },


        fallbacks=[CommandHandler('cancle', cancel)]
    )

    dp.add_handler(conv_handler)

    dp.add_handler(CallbackQueryHandler(quiz, pattern ='^' + 'start' + '$'))
    
    dp.add_error_handler(error)

#  webhook_url should change when i restart ngrok
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='https://0b22-104-223-103-85.ngrok.io/' + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
