from telegram import (Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (CallbackContext, ConversationHandler)
import os, logging # for enhanced logging do not use print!!

# custom modules import
# from modules import dbmodel, mongoDumpModule
# from modules.mongoDriver import DB_connection, DB_rdkit_connection
# import restrictions decorator
# from modules.administration import restricted
from token_extractor import token

from random_word import RandomWords

def wordgenerator():
    
    r = RandomWords()
    word = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun")
    return word

def start(update, context):
    """
    welcome message and launching the game
    """
    word = wordgenerator()
    while ("-" in word) or (" " in word) or type(word) == 'NoneType':
        word = wordgenerator()
        continue
    # retrieving data from user message
    chat_id = update.message.chat.id
    user_info = update.message.from_user
    # приветственное сообщение юзеру
    update.message.reply_text(
"""Привет, {}! 👩🏻‍💻 \nstarting word for you is {}""".format(user_info.first_name, word))
       
 
    # # запись данных юзера в БД 
    # userdata_dict = {
    #     "_id": user_info.id,
    #     "user_id": user_info.id,
    #     "username": "@{}".format(user_info.username),
    #     "firstname": user_info.first_name,
    #     "lastname": user_info.last_name
    # }
    # dbmodel.add_user_record(DB_connection, **userdata_dict)

    # associated with user chat and context stored data should be cleaned up to prevent mess
    context.chat_data.clear()
    user_data = context.user_data
    user_data.clear()

    # test logging module
    logging.info('user initialized by /start command.')
    return -1 # equivalent of ConversationHandler.END : to be able to end conversation with this /start function


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    user_info = update.message.from_user
    update.message.reply_text(('''Привет, {}! 👩🏻‍💻
/start - приветствие 
/purge_handler - очистка бд
/help - эхо-тест
/dump - тестирование дампа базы данных (присылает в лс зип-дамп)
/update - заполняет базу вендоров фрагментами''').format(user_info.first_name))


def exit(update, context):
    """
    hadler for terminating all dialog sequences
    """
    # now clear all cached data
    # clear assosiated with user data and custom context variables
    context.chat_data.clear()
    context.user_data.clear()
    # equivalent of return ConversationHandler.END
    return ConversationHandler.END
