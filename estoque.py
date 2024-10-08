import sqlite3

def conectar_db():
    conn = sqlite3.connect('estoque.db')
    return conn

def criar_tabela():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco REAL NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def adicionar_produto(nome, categoria, quantidade, preco):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO produtos (nome, categoria, quantidade, preco)
    VALUES (?, ?, ?, ?)
    ''', (nome, categoria, quantidade, preco))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def atualizar_produto(id, nome, categoria, quantidade, preco):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE produtos
    SET nome = ?, categoria = ?, quantidade = ?, preco = ?
    WHERE id = ?
    ''', (nome, categoria, quantidade, preco, id))
    conn.commit()
    conn.close()

def remover_produto(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Cria a tabela ao iniciar o script
criar_tabela()
