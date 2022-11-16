from flask import Blueprint, render_template, request, redirect, url_for
from mod_compartilhado.funcoes import Funcoes
import requests

bp_cliente = Blueprint(
    'cliente', __name__, url_prefix="/cliente", template_folder='templates')


urlApiClientes = "http://localhost:8000/cliente/"
urlApiCliente = "http://localhost:8000/cliente/%s"
headers = {'x-token': 'abcBolinhasToken', 'x-key': 'abcBolinhasKey'}


@bp_cliente.route('/', methods=['GET', 'POST'])
def formListaCliente():
    try:
        response = requests.get(urlApiClientes, headers=headers)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result)
        return render_template('formListaCliente.html', result=result)
    except Exception as e:
        return render_template('formListaCliente', erro=e)


@bp_cliente.route('/form-cliente/', methods=['GET', 'POST'])
def formCliente():
    return render_template('formCliente.html')


@bp_cliente.route('/insert', methods=['POST'])
def insert():
    try:
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        compra_fiado = request.form['compra_fiado']
        dia_fiado = request.form['dia_fiado']
        if (compra_fiado == 0):
            dia_fiado = None

        senha = Funcoes.cifrarSenha(request.form['senha'])

        if 'compra_fiado' in request.form:
            dia_fiado = request.form['compra_fiado']

        payload = {
            'nome': nome,
            'cpf': cpf,
            'telefone': telefone,
            'senha': senha,
            'compra_fiado': compra_fiado,
            'dia_fiado': dia_fiado
        }

        response = requests.post(
            urlApiClientes, headers=headers, json=payload)
        result = response.json()

        return redirect(url_for('cliente.formListaCliente', msg=result))

    except Exception as e:
        return redirect(url_for('cliente.formListaCliente', msgErro=e))
