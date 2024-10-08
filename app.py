from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados SQLite
def conectar_bd():
    return sqlite3.connect('estoque.db')

# Função para obter produtos com filtro de pesquisa
def obter_produtos(pesquisa=None):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    if pesquisa:
        cursor.execute("SELECT id, nome, categoria, quantidade, preco, estoque_minimo FROM produtos WHERE nome LIKE ?", (f'%{pesquisa}%',))
    else:
        cursor.execute("SELECT id, nome, categoria, quantidade, preco, estoque_minimo FROM produtos")
    produtos = cursor.fetchall()
    conexao.close()
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
def atualizar_estoque(produto_id, quantidade, preco, estoque_minimo):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET quantidade = ?, preco = ?, estoque_minimo = ? WHERE id = ?", 
                   (quantidade, preco, estoque_minimo, produto_id))
    conn.commit()
    conn.close()

# Função para excluir um produto do banco de dados
def excluir_produto(produto_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()

# Página inicial que exibe a lista de produtos e a opção de adicionar e editar produtos
@app.route('/', methods=['GET'])
def index():
    pesquisa = request.args.get('pesquisa')
    produtos = obter_produtos(pesquisa)
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
    cursor.execute("SELECT id, nome, quantidade, preco, estoque_minimo FROM produtos WHERE id = ?", (id,))
    produto = cursor.fetchone()
    conn.close()
    return render_template('editar.html', produto=produto)

# Rota para salvar as alterações de estoque
@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])  # Adiciona a obtenção do preço
    estoque_minimo = int(request.form['estoque_minimo'])
    atualizar_estoque(id, quantidade, preco, estoque_minimo)
    return redirect('/')

# Rota para excluir um produto
@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    excluir_produto(id)  # Chama a função para excluir o produto
    return redirect('/')  # Redireciona para a página inicial após excluir

if __name__ == '__main__':
    app.run(debug=True)
