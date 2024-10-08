import sqlite3

# Função para conectar ao banco de dados
def conectar_bd():
    conn = sqlite3.connect('estoque.db')  # Altere para o nome do seu banco de dados
    conn.row_factory = sqlite3.Row  # Para acessar os dados por nome de coluna
    return conn
