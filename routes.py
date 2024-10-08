# routes.py
from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

# Criando um blueprint para as rotas
bp = Blueprint('routes', __name__)

# Função para conectar ao banco de dados
def conectar_bd():
    conn = sqlite3.connect('estoque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota principal que exibe todos os produtos
@bp.route('/', methods=['GET', 'POST'])
def index():
    conn = conectar_bd()
    cursor = conn.cursor()

    if request.method == 'POST':
        pesquisa = request.form['pesquisa']
        cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", ('%' + pesquisa + '%',))
        produtos = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()

    conn.close()
    return render_template('index.html', produtos=produtos)

# Rota para exibir o formulário de edição de estoque
@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = conectar_bd()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        estoque_minimo = request.form['estoque_minimo']
        preco = request.form['preco']

        cursor.execute("""
            UPDATE produtos
            SET nome = ?, quantidade = ?, estoque_minimo = ?, preco = ?
            WHERE id = ?
        """, (nome, quantidade, estoque_minimo, preco, id))
        conn.commit()
        conn.close()
        return redirect(url_for('routes.index'))

    cursor.execute("SELECT id, nome, quantidade, estoque_minimo, preco FROM produtos WHERE id = ?", (id,))
    produto = cursor.fetchone()
    conn.close()

    if produto is None:
        return "Produto não encontrado", 404

    return render_template('editar.html', produto=produto)

# Rota para atualizar os dados do produto
@bp.route('/atualizar/<int:id>', methods=['POST'])
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
        SET nome = ?, quantidade = ?, estoque_minimo = ?, preco = ?
        WHERE id = ?
    """, (nome, quantidade, estoque_minimo, preco, id))
    conn.commit()  # Confirma as alterações
    conn.close()  # Fecha a conexão

    return redirect(url_for('routes.index'))  # Redireciona para a página inicial
