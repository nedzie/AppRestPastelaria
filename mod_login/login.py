from flask import Blueprint, render_template, request, redirect, url_for, session
from mod_compartilhado.funcoes import Funcoes
from functools import wraps
import requests

bp_login = Blueprint('login', __name__, url_prefix='/',
                     template_folder='templates')

headers = {'x-token': 'abcBolinhasToken', 'x-key': 'abcBolinhasKey'}
url_login = "http://localhost:8000/teste/"


@bp_login.route("/", methods=['GET', 'POST'])
def login():
    return render_template("formLogin.html")


@bp_login.route('/login', methods=['POST'])
def validaLogin():
    try:
        cpf = request.form['usuario']
        senha = Funcoes.cifrarSenha(request.form['senha'])

        payload = {
            'cpf': cpf,
            'senha': senha
        }

        session.clear()

        autenticado = requests.post(
            url_login, headers=headers, params=payload)

        res = autenticado.json()
        print(res)

        if (res[0] is 1):
            usuario = res[1]
            session['login'] = usuario['nome']
            usuario = usuario['grupo']
            if (usuario == 1):
                usuario = 'Atendente'
            elif (usuario == 2):
                usuario = 'Caixa'
            elif (usuario == 3):
                usuario = 'Administrador'

            print(usuario)
            session['usuario'] = usuario
            return redirect(url_for('index.index'))
        else:
            raise Exception(
                "Falha de Login! Verifique seus dados e tente novamente!")
    except Exception as e:
        return redirect(url_for('login.login', msgErro=e.args[0]))


def validaSessao(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            return redirect(url_for('login.login', msgErro='Usuário não logado!'))
        else:
            return f(*args, **kwargs)
    return decorated_function


@bp_login.route('/logoff', methods=['GET'])
def logoff():
    session.pop('login', None)

    session.clear()

    return redirect(url_for('login.login'))
