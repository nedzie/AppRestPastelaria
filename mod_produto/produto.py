from flask import Blueprint, render_template, request, redirect, url_for
import requests
import base64


bp_produto = Blueprint(
    'produto', __name__, url_prefix="/produto", template_folder='templates')


''' endereços de endpoint '''
urlApiProdutos = "http://localhost:8000/produto"
urlApiProduto = "http://localhost:8000/produto/%s"
headers = {'x-token': 'abcBolinhasToken', 'x-key': 'abcBolinhasKey'}


@bp_produto.route('/', methods=['GET', 'POST'])
def formListaProduto():
    try:
        response = requests.get(urlApiProdutos, headers=headers)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result)
        return render_template('formListaProduto.html', result=result)
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e)


@bp_produto.route('/form-produto/', methods=['GET'])
def formProduto():
    return render_template('formProduto.html')


@bp_produto.route('/insert', methods=['POST'])
def insert():
    try:
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor_unitario = request.form['valor_unitario']
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(
            base64.b64encode(request.files['foto'].read()), "utf-8")

        payload = {
            'nome': nome,
            'descricao': descricao,
            'foto': foto,
            'valor_unitario': valor_unitario
        }

        response = requests.post(urlApiProdutos, headers=headers, json=payload)
        result = response.json()

        return redirect(url_for('produto.formListaProduto', msg=result))
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e)
