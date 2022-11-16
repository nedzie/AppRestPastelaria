from flask import Blueprint, render_template, request, redirect, url_for
from mod_compartilhado.funcoes import Funcoes
import requests

bp_funcionario = Blueprint(
    'funcionario', __name__, url_prefix="/funcionario", template_folder='templates')


''' endereços do endpoint, dentro de variáveis '''
urlApiFuncionarios = "http://localhost:8000/funcionario/"
urlApiFuncionario = "http://localhost:8000/funcionario/%s"
headers = {'x-token': 'abcBolinhasToken', 'x-key': 'abcBolinhasKey'}

''' rotas utilizando as variáveis '''


@bp_funcionario.route('/', methods=['GET', 'POST'])
def formListaFuncionario():
    try:
        response = requests.get(urlApiFuncionarios, headers=headers)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result)
        return render_template('formListaFuncionario.html', result=result)
    except Exception as e:
        return render_template('formListaFuncionario.html', erro=e)


@bp_funcionario.route('/form-funcionario/', methods=['GET'])
def formFuncionario():
    return render_template('formFuncionario.html')


@bp_funcionario.route('/insert', methods=['POST'])
def insert():
    try:
        # atribui os dados do form para as variáveis
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        senha = Funcoes.cifrarSenha(request.form['senha'])

        # criação do objeto para ser enviado a API
        payload = {
            'nome': nome,
            'matricula': matricula,
            'cpf': cpf,
            'telefone': telefone,
            'grupo': grupo,
            'senha': senha
        }

        response = requests.post(
            urlApiFuncionarios, headers=headers, json=payload)
        result = response.json()

        return redirect(url_for('funcionario.formListaFuncionario', msg=result))
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e)
