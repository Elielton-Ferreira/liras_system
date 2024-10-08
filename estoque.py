from flask import Flask, render_template, request, redirect  # Importa as classes e funções necessárias do Flask
import sqlite3  # Importa a biblioteca sqlite3 para interagir com o banco de dados SQLite

app = Flask(__name__)  # Cria uma instância da aplicação Flask

# Função para conectar ao banco de dados SQLite
def conectar_bd():
    return sqlite3.connect('estoque.db')  # Retorna uma conexão com o banco de dados 'estoque.db'

# Função para obter produtos com filtro de pesquisa
def obter_produtos(pesquisa=None):
    conexao = conectar_bd()  # Conecta ao banco de dados
    cursor = conexao.cursor()  # Cria um cursor para executar comandos SQL
    
    # Se uma pesquisa for fornecida, filtra os produtos
    if pesquisa:
        cursor.execute("SELECT id, nome, categoria, quantidade, preco, estoque_minimo FROM produtos WHERE nome LIKE ?", (f'%{pesquisa}%',))
    else:
        cursor.execute("SELECT id, nome, categoria, quantidade, preco, estoque_minimo FROM produtos")  # Seleciona todos os produtos
    
    produtos = cursor.fetchall()  # Obtém todos os resultados da consulta
    conexao.close()  # Fecha a conexão com o banco de dados
    return produtos  # Retorna a lista de produtos

# Função para adicionar um novo produto ao banco de dados
def adicionar_produto(nome, categoria, quantidade, preco, estoque_minimo):
    conn = conectar_bd()  # Conecta ao banco de dados
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute("INSERT INTO produtos (nome, categoria, quantidade, preco, estoque_minimo) VALUES (?, ?, ?, ?, ?)",
                   (nome, categoria, quantidade, preco, estoque_minimo))  # Executa a consulta para inserir um novo produto
    conn.commit()  # Salva as mudanças no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

# Função para atualizar o estoque de um produto
def atualizar_estoque(produto_id, quantidade, estoque_minimo):
    conn = conectar_bd()  # Conecta ao banco de dados
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute("UPDATE produtos SET quantidade = ?, estoque_minimo = ? WHERE id = ?", 
                   (quantidade, estoque_minimo, produto_id))  # Executa a consulta para atualizar a quantidade e o estoque mínimo do produto
    conn.commit()  # Salva as mudanças no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

# Página inicial que exibe a lista de produtos e a opção de adicionar e editar produtos
@app.route('/', methods=['GET'])  # Certifique-se de que a rota aceita apenas GET
def index():
    pesquisa = request.args.get('pesquisa')  # Obtém o parâmetro de pesquisa da URL
    produtos = obter_produtos(pesquisa)  # Obtém os produtos, filtrando se necessário
    return render_template('index.html', produtos=produtos)  # Renderiza o template 'index.html' passando a lista de produtos

# Rota para exibir o formulário de adicionar produto (GET) e adicionar o produto (POST)
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method =
