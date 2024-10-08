from flask import Flask, render_template, request, redirect
from estoque import listar_produtos, adicionar_produto, atualizar_produto, remover_produto

app = Flask(__name__)

@app.route('/')
def index():
    produtos = listar_produtos()
    return render_template('index.html', produtos=produtos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    quantidade = request.form['quantidade']
    preco = request.form['preco']
    adicionar_produto(nome, categoria, quantidade, preco)
    return redirect('/')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        quantidade = request.form['quantidade']
        preco = request.form['preco']
        atualizar_produto(id, nome, categoria, quantidade, preco)
        return redirect('/')
    
    # Obter os dados do produto a ser editado
    produtos = listar_produtos()
    produto = next((p for p in produtos if p[0] == id), None)
    return render_template('editar.html', produto=produto)

@app.route('/remover/<int:id>')
def remover(id):
    remover_produto(id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
