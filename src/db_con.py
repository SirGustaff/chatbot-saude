import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',       
    'password': '12345678',     
    'database': 'consulta'      
}

def adicionar_consulta(nome, data, horario, user_id, local, especialidade):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO consulta (nome, data, horario, user_id, local, especialidade)
    VALUES (%s, %s, %s, %s, %s, %s)
    ''', (nome, data, horario, user_id, local, especialidade))
    conn.commit()
    conn.close()

def obter_consultas(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT nome, data, horario, local, especialidade
    FROM consulta
    WHERE user_id = %s
    ORDER BY data ASC, horario ASC
    ''', (user_id,))

    consultas = cursor.fetchall()
    conn.close()
    
    return consultas
