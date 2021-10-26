#!/usr/bin/env python
# pylint: disable=C0116

"""
Usage:
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the bot.
"""

import logging, requests, json

from telegram import (
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove, 
    Update, 
    ForceReply, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)

global Endpoint, Headers, updater, dispatcher
updater=""
dispatcher=""
Endpoint = "http://IP_ADDR:9000/"
Headers = {"Authorization": "Bearer THE_HIVE_API_KEY"}
Telegram_Key = "TELEGRAM_API_KEY"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

## Basic Functionality
def start(update: Update, _: CallbackContext) -> str:
    user = update.effective_user
    update.message.reply_text(
        f'Hi {user.first_name}! My name is SocBot. How can I be of assistance?'
        ' Send /help for a list of commands.\n\n'
    )

def help_command(update: Update, _ : CallbackContext) -> str:
    user = update.effective_user
    logger.info("User %s requested a list of commands.", user.first_name)
    update.message.reply_text(
        'The current functionality is listed below:\n\n '
        '- /help: for a list of commands.\n'
        '- /th: provides a keyboard with the current Case Management functionality.\n'
        '- /vt <IoC>: to run a check against VirusTotal.\n'
    )

def unknown(update: Update, _: CallbackContext) -> str:
    user = update.effective_user
    logger.info("User %s initiated unknown command.", user.first_name)
    update.message.reply_text(
        "Sorry, I don't understand the command. Please type /help for a list of commands."
    )

## Case Management with TheHive
### Idea: User prompts for different information which can then be sent to TheHive

def get_case() -> json: 
    message_url = Endpoint + 'api/case'
    return requests.get(message_url,headers=Headers)

def create_case(prepared_data) -> json:
    message_url = Endpoint + 'api/case'
    return requests.post(message_url, data=prepared_data, headers=Headers)
     
def update_case(prepared_data, caseId) -> json:
    message_url = Endpoint + f'api/case/{caseId}'  
    return requests.patch(message_url,data=prepared_data,headers=Headers)   

def delete_case(caseId) -> json:
    message_url = Endpoint + f'api/case/{caseId}'
    return requests.delete(message_url,headers=Headers)

## GET THEHIVE CASES
def print_cases(chat_id, cases, context):
    active_case = cases.json()
    context.bot.send_message(chat_id=chat_id,text="=================== Open Cases ===================")
    for case in active_case:
        if(case['status'] == "Open"):
            context.bot.send_message(chat_id=chat_id,text="Owner:\t" + str(case['owner']))
            context.bot.send_message(chat_id=chat_id,text="Title:\t" + str(case['title']))
            context.bot.send_message(chat_id=chat_id,text="Identifier:\t" + str(case['id']) + "\n")
            #context.bot.send_message(chat_id=chat_id,text=case)
    context.bot.send_message(chat_id=chat_id, text="========================================")

## CREATE NEW THEHIVE CASE
def create_cases(chat_id, context):
    case_data = {
        'title': 'My Second Python Case',
        'description': 'This case has been created by my custom Python Script'
    }
    case = create_case(case_data).json()
    context.bot.send_message(chat_id=chat_id,text="=================== New Case ===================")
    context.bot.send_message(chat_id=chat_id,text=case)

## DELETE THEHIVE CASE
def delete_cases(chat_id, caseId, context):
    deleted_case = delete_case(caseId)
    context.bot.send_message(chat_id=chat_id,text="\n=================== Deleted Case {caseId} ===================\n")

## UPDATE THEHIVE CASE
def update_cases(chat_id,caseId, context):
    case_data = {
        'tlp': 3
    }
    updated_case = update_case(case_data, caseId).json()
    context.bot.send_message(chat_id=chat_id,text="\n=================== Updated Case {caseId} ===================\n")
    context.bot.send_message(chat_id=chat_id,text=updated_case)

## In-Line Keyboard
def keyboard(update: Update, _: CallbackContext) -> None:
    """Show TheHive choices using buttons"""
    keyboard = [
        [
            InlineKeyboardButton("Create", callback_data=str(create_case)),
            InlineKeyboardButton("Get", callback_data=str(get_case)),
            InlineKeyboardButton("Update", callback_data=str(update_case)),
            InlineKeyboardButton("Delete", callback_data=str(delete_case)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update: Update, _: CallbackContext) -> str:
    user = update.effective_user
    logger.info("User %s is accessing TheHive", user.first_name)   
    query = update.callback_query
    query.answer()

    chat_id = update.effective_chat.id
    if "get_case" in query.data:
        cases = get_case()
        print_cases(chat_id,cases, _) 

def main() -> None:
    # Create the Updater and pass it your bot's token.
    global updater, dispatcher
    updater = Updater(Telegram_Key)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Answer in Telegram for basic commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("th", keyboard))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    ## Need to create a conversational handler - perhaps prompt for a keyboard with the different options. Then start a conversation with the person asking for info.
    ### https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py
    dispatcher.add_handler(CommandHandler("create", create_case))
    dispatcher.add_handler(CommandHandler("get", get_case))
    dispatcher.add_handler(CommandHandler("update", update_case))
    dispatcher.add_handler(CommandHandler("delete", delete_case))

    # Answer in Telegram for commands that don't exist
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, unknown))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
