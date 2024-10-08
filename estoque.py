import sqlite3

# Função para obter produtos com seus dados, incluindo estoque mínimo
def obter_produtos():
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, categoria, quantidade, preco, estoque_minimo FROM produtos")
    produtos = cursor.fetchall()
    conexao.close()
    return produtos

# Função para atualizar o estoque mínimo de um produto
def atualizar_estoque_minimo(produto_id, novo_estoque_minimo):
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute("UPDATE produtos SET estoque_minimo = ? WHERE id = ?", (novo_estoque_minimo, produto_id))
    conexao.commit()
    conexao.close()
