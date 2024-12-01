# This example show how to use inline keyboards and process button presses
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.ia import Ia

TELEGRAM_TOKEN = '7746958558:AAEJLybNX4Okj6tkkRpPlepwKxn5tZ7wHgk'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
                               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup



@bot.message_handler(commands=["show_id"])
def show_user_id(mensagem):
    user_id = mensagem.from_user.id  # Get the user's unique ID
    bot.reply_to(mensagem, f"Hello! Your User ID is {user_id}")

bot.infinity_polling()