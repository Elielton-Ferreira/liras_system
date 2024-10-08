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
    
    # Se uma pesquisa for fornecida, filtra os produtos
    if pesquisa:
        cursor.execute("SELECT id, nome, categoria, quantidade, preco, estoque_minimo FROM produtos WHERE nome LIKE ?", (f'%{pesquisa}%',))
    else:
        cursor.execute("SELECT id, nome, categoria, quantidade, preco, estoque_minimo FROM produtos")
    
    produtos = cursor.fetchall()  # Obtém todos os produtos
    conexao.close()  # Fecha a conexão com o banco de dados
    return produtos  # Retorna a lista de produtos

# Função para adicionar um novo produto ao banco de dados
def adicionar_produto(nome, categoria, quantidade, preco, estoque_minimo):
    conn = conectar_bd()
    cursor = conn.cursor()
    # Insere um novo produto na tabela produtos
    cursor.execute("INSERT INTO produtos (nome, categoria, quantidade, preco, estoque_minimo) VALUES (?, ?, ?, ?, ?)",
                   (nome, categoria, quantidade, preco, estoque_minimo))
    conn.commit()  # Salva as mudanças no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

# Função para atualizar o estoque de um produto
def atualizar_estoque(produto_id, quantidade, estoque_minimo, preco):
    conn = conectar_bd()
    cursor = conn.cursor()
    # Atualiza a quantidade, estoque mínimo e preço do produto na tabela produtos
    cursor.execute("UPDATE produtos SET quantidade = ?, estoque_minimo = ?, preco = ? WHERE id = ?", 
                   (quantidade, estoque_minimo, preco, produto_id))
    conn.commit()  # Salva as mudanças no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

# Página inicial que exibe a lista de produtos e a opção de adicionar e editar produtos
@app.route('/', methods=['GET'])
def index():
    pesquisa = request.args.get('pesquisa')  # Obtém o termo de pesquisa da query string
    produtos = obter_produtos(pesquisa)  # Obtém os produtos, filtrando se necessário
    return render_template('index.html', produtos=produtos)  # Renderiza a página principal

# Rota para exibir o formulário de adicionar produto (GET) e adicionar o produto (POST)
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':  # Se o método da requisição for POST
        # Obtém os dados do formulário
        nome = request.form['nome']
        categoria = request.form['categoria']
        quantidade = int(request.form['quantidade'])
        preco = float(request.form['preco'])
        estoque_minimo = int(request.form['estoque_minimo'])
        # Adiciona o produto ao banco de dados
        adicionar_produto(nome, categoria, quantidade, preco, estoque_minimo)
        return redirect('/')  # Redireciona para a página inicial
    return render_template('adicionar_produto.html')  # Renderiza a página de adicionar produto

# Rota para exibir o formulário de edição de estoque
@app.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    # Obtém o produto a ser editado
    cursor.execute("SELECT id, nome, quantidade, estoque_minimo, preco FROM produtos WHERE id = ?", (id,))
    produto = cursor.fetchone()  # Obtém os dados do produto
    conn.close()  # Fecha a conexão com o banco de dados
    return render_template('editar.html', produto=produto)  # Renderiza a página de edição

# Rota para salvar as alterações de estoque
@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    # Obtém os dados do formulário
    quantidade = int(request.form['quantidade'])
    estoque_minimo = int(request.form['estoque_minimo'])
    preco = float(request.form['preco'])  # Obtém o novo preço do formulário
    # Atualiza o estoque e o preço do produto
    atualizar_estoque(id, quantidade, estoque_minimo, preco)  
    return redirect('/')  # Redireciona para a página inicial

if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor em modo de depuração
