from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados SQLite
def conectar_bd():
    return sqlite3.connect('estoque.db')

# Função para obter todos os produtos do banco de dados
def obter_produtos():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, categoria, quantidade, preco, estoque_minimo FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return produtos

# Função para adicionar um novo produto ao banco de dados
def adicionar_produto(nome, categoria, quantidade, preco, estoque_minimo):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, categoria, quantidade, preco, estoque_minimo) VALUES (?, ?, ?, ?, ?)",
                   (nome, categoria, quantidade, preco, estoque_minimo))
    conn.commit()
    conn.close()

# Função para atualizar o estoque de um produto
def atualizar_estoque(produto_id, quantidade, estoque_minimo):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET quantidade = ?, estoque_minimo = ? WHERE id = ?", 
                   (quantidade, estoque_minimo, produto_id))
    conn.commit()
    conn.close()

# Página inicial que exibe a lista de produtos e a opção de adicionar e editar produtos
@app.route('/')
def index():
    produtos = obter_produtos()
    return render_template('index.html', produtos=produtos)

# Rota para exibir o formulário de adicionar produto (GET) e adicionar o produto (POST)
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        quantidade = int(request.form['quantidade'])
        preco = float(request.form['preco'])
        estoque_minimo = int(request.form['estoque_minimo'])
        adicionar_produto(nome, categoria, quantidade, preco, estoque_minimo)
        return redirect('/')
    return render_template('adicionar_produto.html')

# Rota para exibir o formulário de edição de estoque
@app.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, quantidade, estoque_minimo FROM produtos WHERE id = ?", (id,))
    produto = cursor.fetchone()
    conn.close()
    return render_template('editar.html', produto=produto)

# Rota para salvar as alterações de estoque
@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    quantidade = int(request.form['quantidade'])
    estoque_minimo = int(request.form['estoque_minimo'])
    atualizar_estoque(id, quantidade, estoque_minimo)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
