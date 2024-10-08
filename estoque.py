import sqlite3  # Importa a biblioteca sqlite3 para interagir com o banco de dados SQLite

# Função para obter produtos com seus dados, incluindo estoque mínimo
def obter_produtos():
    conexao = sqlite3.connect('estoque.db')  # Conecta ao banco de dados 'estoque.db'
    cursor = conexao.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute("SELECT id, nome, categoria, quantidade, preco, estoque_minimo FROM produtos")  # Executa a consulta para selecionar todos os produtos
    produtos = cursor.fetchall()  # Obtém todos os resultados da consulta
    conexao.close()  # Fecha a conexão com o banco de dados
    return produtos  # Retorna a lista de produtos

# Função para atualizar o estoque mínimo de um produto
def atualizar_estoque_minimo(produto_id, novo_estoque_minimo):
    conexao = sqlite3.connect('estoque.db')  # Conecta ao banco de dados 'estoque.db'
    cursor = conexao.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute("UPDATE produtos SET estoque_minimo = ? WHERE id = ?", (novo_estoque_minimo, produto_id))  # Executa a consulta para atualizar o estoque mínimo do produto pelo ID
    conexao.commit()  # Salva as mudanças no banco de dados
    conexao.close()  # Fecha a conexão com o banco de dados
