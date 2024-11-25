from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def diagnostico_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Sim", callback_data="dg_sim"),
                               InlineKeyboardButton("Não", callback_data="dg_nao"))
    return markup

