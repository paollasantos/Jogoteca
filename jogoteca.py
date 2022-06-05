from flask import Flask, render_template, request, redirect, session, flash, url_for  

from models import Jogo, Usuario
from dao import JogoDao
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'alura'

app.config['MYSQL_HOST'] = "127.0.0.1"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "MYSQL"
app.config['MYSQL_DB'] = "jogoteca"
app.config['MYSQL_PORT'] = 3306

db = MySQL(app)

Jogo_dao = JogoDao(db)

# nome de classe começa sempre com a primeira letra maiuscula

jogo1= Jogo('GTA V', 'Ação/Aventura' , 'PC')
jogo2= Jogo('FIFA' , 'Futebol' , 'Xbox one')
jogo3= Jogo('Mortal Kombat' , 'Luta' , 'PS2')
lista = [jogo1 , jogo2 , jogo3]


usuario1 = Usuario('Paola Santos', 'PS', 'santos10')
usuario2 = Usuario('Bruno Moreira', 'BM', 'moreira10')
usuario3 = Usuario('Lennon Lima', 'LL', 'lennon123')

usuarios = {usuario1.nickname : usuario1,
            usuario2.nickname : usuario2,
            usuario3.nickname : usuario3}


@app.route("/")
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route("/novo")
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome,categoria,console)
    Jogo_dao.salvar(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nome + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else: 
        flash('usuário não logado')
        return redirect(url_for('login'))  

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('logout efetuado com sucesso!') 
    return redirect(url_for('index'))

app.run(debug = True)
