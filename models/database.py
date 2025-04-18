import sqlite3

def conectar_bd():
    conn = sqlite3.connect('estoque.db')
    conn.row_factory = sqlite3.Row
    return conn
