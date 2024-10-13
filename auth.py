from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import time

auth = Blueprint('auth', __name__)

# Duração da sessão em segundos
SESSION_DURATION = 300  # 5 minutos

# Função para conectar ao banco de dados
def conectar_bd():
    conn = sqlite3.connect('estoque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Decorador para verificar a sessão
def require_login(f):
    def wrapper(*args, **kwargs):
        if 'username' not in session or time.time() - session.get('last_activity', 0) > SESSION_DURATION:
            return redirect(url_for('login'))  # Redireciona para a tela de login
        session['last_activity'] = time.time()  # Atualiza a hora da última atividade
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__  # Manter o nome da função original
    return wrapper

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username  # Armazena o nome de usuário na sessão
            session['last_activity'] = time.time()  # Marca a hora da atividade
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))  # Redireciona para a página inicial
        else:
            flash('Usuário ou senha inválidos!', 'danger')

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('username', None)  # Remove o usuário da sessão
    flash('Você foi desconectado.', 'success')
    return redirect(url_for('login'))

@auth.route('/some_protected_route')  # Exemplo de uma rota protegida
@require_login
def some_protected_route():
    return render_template('some_protected_template.html')
