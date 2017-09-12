import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job

import os
import keys
import random

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    update.message.reply_text(
        'Hi {}'.format(update.message.from_user.first_name))
    schedule_keyboard = [['Once a day', 'Twice a day'],
                         ['Once a week', 'Never']]
    reply_markup = telegram.ReplyKeyboardMarkup(schedule_keyboard, 
                                                one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, 
                     text="Choose a turtle delivery frequency", 
                     reply_markup=reply_markup)

def stop(bot, update):
    jobs[update.message.chat_id].schedule_removal()
    bot.send_message(chat_id=update.message.chat_id, 
                     text="Turtle delivered stopped")

def turtle(bot, update):
    print "turtle"
    send_turtle(bot, update.message.chat_id)

def send_turtle(bot, c_id):
    bot.send_chat_action(chat_id=c_id,
                         action=telegram.ChatAction.TYPING)

    turtle_photos = os.listdir('turtles')
    rand_turtle = turtle_photos[random.randint(0, len(turtle_photos)-1)]
    if '.gif' in rand_turtle:
        print "gif"
        bot.send_document(chat_id=c_id,
                          document=open('turtles/{}'.format(rand_turtle)))
    else:
        bot.send_photo(chat_id=c_id,
                       photo=open('turtles/{}'.format(rand_turtle)))

def turtle_callback(bot, job):
    send_turtle(bot, job.context)

def parse_message_response(bot, update, job_queue):
    print "test"
    chat_id = update.message.chat_id
    user_response = update.message.text.lower()

    if user_response == "fast":
        job = Job(turtle_callback, 10.0, context=chat_id)
        jobs[chat_id] = job
        jq.put(job, next_t=0.0)
    elif user_response == "once a day":
        job = Job(turtle_callback, 60*60*24, context=chat_id)
        jobs[chat_id] = job
        jq.put(job, next_t=0.0)
    elif user_response == "twice a day":
        job = Job(turtle_callback, 60*30*24, context=chat_id)
        jobs[chat_id] = job
        jq.put(job, next_t=0.0)
    elif user_response == "once a week":
        job = Job(turtle_callback, 60*60*24*7, context=chat_id)
        jobs[chat_id] = job
        jq.put(job, next_t=0.0)
    elif user_response == "stop" or user_response == "never":
        stop(bot, update)

updater = Updater(keys.bot_key)

jobs = {}
jq = updater.job_queue
dp = updater.dispatcher

# Cat A Day Handlers
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('stop', stop))
dp.add_handler(CommandHandler('turtle', turtle))

# Message Handlers
dp.add_handler(MessageHandler(Filters.text, parse_message_response, pass_job_queue=True))

updater.start_polling()
updater.idle()