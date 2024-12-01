from src import diagnostico, markup

from src.ia import Ia

import telebot


bot = telebot.TeleBot("7746958558:AAEJLybNX4Okj6tkkRpPlepwKxn5tZ7wHgk", parse_mode=None)

@bot.message_handler(commands=['modo_chat'])
def iniciar_chat(mensagem):
    bot.send_message(
        mensagem.chat.id,
        "Iniciando modo chat, para encerrar digite \"sair\".\n"
        "Estou a seu dispor! Faça qualquer pergunta relacionada a medicina!"
    )

    ia_instance = Ia().iniciar_chat_constante()

    processar_chat_com_ia(mensagem, ia_instance)

def processar_chat_com_ia(mensagem, ia_instance):
    bot.register_next_step_handler(
        mensagem,
        lambda msg: processar_chat(msg, ia_instance) 
    )

def processar_chat(mensagem, ia_instance):
    if mensagem.text.lower() == "sair":
        bot.send_message(mensagem.chat.id, "Modo chat encerrado. Use /modo_chat para reiniciar.")
        return

    resposta = ia_instance.predict(human_input=mensagem.text)

    bot.send_message(mensagem.chat.id, resposta)

    processar_chat_com_ia(mensagem, ia_instance)


@bot.message_handler(commands=['modo_diagnostico'])
def iniciar_diagnostico(mensagem):
    msg = bot.reply_to(mensagem, "Digite o que você está sentindo")
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
     

@bot.message_handler(commands=['start', 'menu'])
def menu_inicial(mensagem):
    texto  = """
Selecione uma das opções para começar:
/modo_chat -> tire todas suas dúvidas referentes a medicina
/modo_diagnostico -> possibilita que você possa receber um diagnóstico rápido segundo seus sintomas
/menu -> permite que você possa ver o menu inicial novamente

	"""
    bot.reply_to(mensagem, texto)


bot.infinity_polling()