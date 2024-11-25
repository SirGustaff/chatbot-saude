from src import diagnostico, markup
import telebot


bot = telebot.TeleBot("7746958558:AAEJLybNX4Okj6tkkRpPlepwKxn5tZ7wHgk", parse_mode=None)

@bot.message_handler(commands=['modo_diagnostico'])
def diagnosticar(mensagem):
    msg = bot.reply_to(mensagem, "Digite aquilo que você está sentindo")
    bot.register_next_step_handler(msg, processar_diagnostico)

def processar_diagnostico(mensagem):
    resultado = diagnostico.efetuar_diagnostico(mensagem.text)
    bot.send_message(mensagem.chat.id, resultado)
    bot.send_message(mensagem.chat.id, "Deseja realizar um novo diagnóstico?" , reply_markup=markup.diagnostico_markup())

@bot.callback_query_handler(func=lambda call: True)
def realizar_novo_diagnostico(call):
    if call.data == "dg_sim":
        bot.answer_callback_query(call.id, "Vamos realizar um novo diagnóstico!")
        msg = bot.send_message(call.message.chat.id, "Digite seus sintomas")
        bot.register_next_step_handler(msg, processar_diagnostico)
    elif call.data == "dg_nao":
        bot.answer_callback_query(call.id, "Diagnóstico encerrado. Obrigado!")
        bot.send_message(call.message.chat.id, "Para retornar ao menu inicial basta selecionar /menu")


@bot.message_handler(commands='modo_chat')
def conversar(mensagem):
    print('')
     

@bot.message_handler(commands=['start', 'menu'])
def menu_inicial(mensagem):
    texto  = """
Selecione uma das opções para começar:
/modo_chat -> tire todas suas dúvidas referentes a medicina
/modo_diagnostico -> possibilita que você possa receber um diagnóstico rápido segundo seus sintomas
/menu -> permite que você possa ver o menu inicial novamente

	"""
    bot.reply_to(mensagem, texto)

@bot.message_handler(func=lambda m: True)
def receber_mensagens(message):
	return message.text;

bot.infinity_polling()