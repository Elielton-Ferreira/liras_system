from flask import Flask, render_template, request, redirect  # Importa as classes e funções necessárias do Flask
import sqlite3  # Importa a biblioteca sqlite3 para interagir com o banco de dados SQLite

app = Flask(__name__)  # Cria uma instância da aplicação Flask

# Função para conectar ao banco de dados SQLite
def conectar_bd():
    return sqlite3.connect('estoque.db')  # Retorna uma conexão com o banco de dados 'estoque.db'

# Função para obter todos os produtos do banco de dados
def obter_produtos():
    conn = conectar_bd()  # Conecta ao banco de dados
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute("SELECT id, nome, categoria, quantidade, preco, estoque_minimo FROM produtos")  # Executa a consulta para selecionar todos os produtos
    produtos = cursor.fetchall()  # Obtém todos os resultados da consulta
    conn.close()  # Fecha a conexão com o banco de dados
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
@app.route('/')
def index():
    produtos = obter_produtos()  # Obtém a lista de produtos
    return render_template('index.html', produtos=produtos)  # Renderiza o template 'index.html' passando a lista de produtos

# Rota para exibir o formulário de adicionar produto (GET) e adicionar o produto (POST)
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':  # Se o método da requisição for POST
        nome = request.form['nome']  # Obtém o nome do produto do formulário
        categoria = request.form['categoria']  # Obtém a categoria do produto do formulário
        quantidade = int(request.form['quantidade'])  # Obtém a quantidade do produto do formulário e converte para inteiro
        preco = float(request.form['preco'])  # Obtém o preço do produto do formulário e converte para float
        estoque_minimo = int(request.form['estoque_minimo'])  # Obtém o estoque mínimo do produto do formulário e converte para inteiro
        adicionar_produto(nome, categoria, quantidade, preco, estoque_minimo)  # Adiciona o produto ao banco de dados
        return redirect('/')  # Redireciona para a página inicial após adicionar o produto
    return render_template('adicionar_produto.html')  # Renderiza o template de adicionar produto se o método for GET

# Rota para exibir o formulário de edição de estoque
@app.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    conn = conectar_bd()  # Conecta ao banco de dados
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute("SELECT id, nome, quantidade, estoque_minimo FROM produtos WHERE id = ?", (id,))  # Seleciona o produto pelo ID
    produto = cursor.fetchone()  # Obtém o produto correspondente
    conn.close()  # Fecha a conexão com o banco de dados
    return render_template('editar.html', produto=produto)  # Renderiza o template de edição passando o produto

# Rota para salvar as alterações de estoque
@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    quantidade = int(request.form['quantidade'])  # Obtém a nova quantidade do produto do formulário e converte para inteiro
    estoque_minimo = int(request.form['estoque_minimo'])  # Obtém o novo estoque mínimo do produto do formulário e converte para inteiro
    atualizar_estoque(id, quantidade, estoque_minimo)  # Atualiza o estoque do produto no banco de dados
    return redirect('/')  # Redireciona para a página inicial após atualizar o estoque

if __name__ == '__main__':
    app.run(debug=True)  # Executa a aplicação Flask em modo de depuração
