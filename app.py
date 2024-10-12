from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessário para exibir mensagens flash

# Função para conectar ao banco de dados
def conectar_bd():
    conn = sqlite3.connect('estoque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota principal que exibe todos os produtos
@app.route('/', methods=['GET', 'POST'])
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

# Rota para adicionar um novo produto
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        quantidade = request.form['quantidade']
        preco = request.form['preco']
        estoque_minimo = request.form['estoque_minimo']

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, categoria, quantidade, preco, estoque_minimo) VALUES (?, ?, ?, ?, ?)",
                       (nome, categoria, quantidade, preco, estoque_minimo))
        conn.commit()
        conn.close()

        flash('Produto adicionado com sucesso!', 'success')  # Mensagem de sucesso
        return redirect(url_for('index'))

    return render_template('adicionar_produto.html')

# Rota para exibir o formulário de edição de estoque
@app.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, quantidade, estoque_minimo, preco FROM produtos WHERE id = ?", (id,))
    produto = cursor.fetchone()
    conn.close()

    if produto is None:
        return "Produto não encontrado", 404

    return render_template('editar.html', produto=produto)

# Rota para atualizar os dados do produto
@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    estoque_minimo = request.form['estoque_minimo']
    preco = request.form['preco']

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produtos
        SET quantidade = ?, estoque_minimo = ?, preco = ?
        WHERE id = ?
    """, (quantidade, estoque_minimo, preco, id))
    conn.commit()
    conn.close()

    flash('Produto atualizado com sucesso!', 'success')  # Mensagem de sucesso
    return redirect(url_for('index'))

# Rota para adicionar um novo vidro
@app.route('/adicionar_vidro', methods=['GET', 'POST'])
def adicionar_vidro():
    if request.method == 'POST':
        nome = request.form['nome']
        altura = float(request.form['altura'])
        largura = float(request.form['largura'])
        preco_m2 = float(request.form['preco_m2'])
        area = altura * largura  # Área em m²

        # Conectar ao banco de dados e inserir o vidro
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vidros (nome, altura, largura, preco_m2, area) VALUES (?, ?, ?, ?, ?)",
                       (nome, altura, largura, preco_m2, area))
        conn.commit()
        conn.close()

        flash(f'Vidro adicionado com sucesso! Área: {area:.2f} m²', 'success')  # Mensagem de sucesso
        return redirect(url_for('adicionar_vidro'))

    return render_template('adicionar_vidro.html')

# Rota para excluir um produto
@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash('Produto excluído com sucesso!', 'success')  # Mensagem de sucesso
    return redirect(url_for('index'))

# Rota para consultar estoque vidros
@app.route('/estoque_vidros', methods=['GET'])
def estoque_vidros():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vidros")
    vidros = cursor.fetchall()
    conn.close()

    return render_template('estoque_vidros.html', vidros=vidros)

# Executa o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
