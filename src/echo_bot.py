from src import diagnostico, markup
from src.db_con import *
from src.ia import Ia

import telebot


bot = telebot.TeleBot("7746958558:AAEJLybNX4Okj6tkkRpPlepwKxn5tZ7wHgk", parse_mode=None)

user_data = {}

@bot.message_handler(commands=['adicionar_consulta'])
def iniciar_adicionar_consulta(message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    bot.send_message(message.chat.id, "Qual é o nome do paciente?")
    bot.register_next_step_handler(message, obter_nome)

def obter_nome(message):
    user_id = message.from_user.id
    user_data[user_id]['nome'] = message.text
    bot.send_message(message.chat.id, "Qual é a data da consulta? (formato YYYY-MM-DD)")
    bot.register_next_step_handler(message, obter_data)

def obter_data(message):
    user_id = message.from_user.id
    user_data[user_id]['data'] = message.text
    bot.send_message(message.chat.id, "Qual é o horário da consulta? (formato HH:MM)")
    bot.register_next_step_handler(message, obter_horario)

def obter_horario(message):
    user_id = message.from_user.id
    user_data[user_id]['horario'] = message.text
    bot.send_message(message.chat.id, "Qual é o local da consulta?")
    bot.register_next_step_handler(message, obter_local)

def obter_local(message):
    user_id = message.from_user.id
    user_data[user_id]['local'] = message.text
    bot.send_message(message.chat.id, "Qual é a especialidade médica?")
    bot.register_next_step_handler(message, obter_especialidade)

def obter_especialidade(message):
    user_id = message.from_user.id
    user_data[user_id]['especialidade'] = message.text

    dados = user_data[user_id]

    nome = dados['nome']
    data = dados['data']
    horario = dados['horario']
    local = dados['local']
    especialidade = dados['especialidade']

    try:
        adicionar_consulta(nome, data, horario, user_id, local, especialidade)

    except mysql.connector.errors.DataError:
        bot.send_message(message.chat.id, "Não foi possível adicionar a consulta! Verifique se os dados estão sendo inseridos no formato correto e tente novamente digitando /adicionar_consulta")
        return

    bot.send_message(message.chat.id, "Consulta adicionada com sucesso! Digite /visualizar_consultas para ver todos os seus agendamentos")
    user_data.pop(user_id, None)



@bot.message_handler(commands=['visualizar_consultas'])
def handle_visualizar_consultas(message):

    consultas = obter_consultas(message.from_user.id)


    if consultas:
        resposta = "Aqui estão suas consultas agendadas:\n\n"
        for c in consultas:
            resposta += f"Nome: {c[0]}\nData: {c[1]}\nHorário: {c[2]}\nLocal: {c[3]}\nEspecialidade: {c[4]}\n\n"
    else:
        resposta = "Você ainda não tem consultas agendadas."

    bot.send_message(message.chat.id, resposta)

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
/adicionar_consulta -> adicionar uma consulta a sua agenda
/visualizar_consultas -> para visualizar suas consultas marcadas
/modo_chat -> tire todas suas dúvidas referentes a medicina
/modo_diagnostico -> possibilita que você possa receber um diagnóstico rápido segundo seus sintomas
/menu -> permite que você possa ver o menu inicial novamente

	"""
    bot.reply_to(mensagem, texto)


bot.infinity_polling()