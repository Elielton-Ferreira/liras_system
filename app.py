from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def conectar_bd():
    conn = sqlite3.connect('estoque.db')  # Altere para o nome do seu banco de dados
    conn.row_factory = sqlite3.Row  # Para acessar os dados por nome de coluna
    return conn

# Rota principal que exibe todos os produtos
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = conectar_bd()
    cursor = conn.cursor()

    # Se houver uma solicitação POST, realiza a pesquisa
    if request.method == 'POST':
        pesquisa = request.form['pesquisa']  # Obtém o termo de pesquisa
        cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", ('%' + pesquisa + '%',))
        produtos = cursor.fetchall()  # Busca produtos que correspondem à pesquisa
    else:
        cursor.execute("SELECT * FROM produtos")  # Busca todos os produtos
        produtos = cursor.fetchall()  # Recupera os dados dos produtos

    conn.close()  # Fecha a conexão
    return render_template('index.html', produtos=produtos)  # Renderiza o template com a lista de produtos

# Rota para exibir o formulário de edição de estoque
@app.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    conn = conectar_bd()
    cursor = conn.cursor()

    # Obtém o produto a ser editado
    cursor.execute("SELECT id, nome, quantidade, estoque_minimo, preco FROM produtos WHERE id = ?", (id,))
    produto = cursor.fetchone()  # Obtém os dados do produto
    conn.close()  # Fecha a conexão

    # Verifica se o produto foi encontrado
    if produto is None:
        return "Produto não encontrado", 404  # Retorna erro se o produto não existir

    return render_template('editar.html', produto=produto)  # Renderiza a página de edição

# Rota para atualizar os dados do produto
@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    # Obtém os dados do formulário
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    estoque_minimo = request.form['estoque_minimo']
    preco = request.form['preco']

    conn = conectar_bd()
    cursor = conn.cursor()
    # Atualiza o produto no banco de dados
    cursor.execute("""
        UPDATE produtos
        SET quantidade = ?, estoque_minimo = ?, preco = ?
        WHERE id = ?
    """, (quantidade, estoque_minimo, preco, id))
    conn.commit()  # Confirma as alterações
    conn.close()  # Fecha a conexão

    return redirect(url_for('index'))  # Redireciona para a página inicial

# Executa o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
