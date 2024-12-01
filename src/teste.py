# This example show how to use inline keyboards and process button presses
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.ia import Ia

TELEGRAM_TOKEN = '7746958558:AAEJLybNX4Okj6tkkRpPlepwKxn5tZ7wHgk'

configuracao = "Você é um assistente que só responde perguntas a medicina, qualquer o tipo de pergunta não deve responder."

ia = Ia()

chat_chain = ia.iniciar_chat_constante(configuracao)

while True:
    pergunta = input("Você: ")
    if pergunta.lower() == "sair":
        print("Chat encerrado.")
        break
    resposta = chat_chain.predict(human_input=pergunta)
    print(resposta)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
                               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())

bot.infinity_polling()