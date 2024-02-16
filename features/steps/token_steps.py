from behave import *
import json
import requests

def generic_acess_endpoint(
    endpoint, 
    data=None, 
    method='GET', 
    headers={'content-type': 'application/json'}
):
    if method == 'GET':
        return requests.get(endpoint, data=data)
    elif method == 'POST':
        return requests.post(endpoint, data=data, headers=headers)

@given(u'um usuário chamado {nome_usuario}')
def step_preencher_nome_usuario(context, nome_usuario):
    context.username = nome_usuario

@given(u'o usuário possui uma senha \'{password}\'')
def step_preencher_password_usuario(context, password):
    context.password = password


@when(u'o usuário acessa o recurso para recuperação de suas informações de token')
def step_recuperar_tokens(context):
    user_data={'password': context.password,'username': context.username}
    context.response  = generic_acess_endpoint("http://localhost:5000/token", data=json.dumps(user_data), method='POST')
    
    
@then(u'o acess_token do usuario é armazenado')
def step_armazenar_acess_token(context):
    assert context.response.status_code in [200,201]
    data = context.response.json()
    assert data
    assert data['access_token']
    assert data['refresh_token']
    assert data['uid']
    context.acess_token = data['access_token']
    context.refresh_token = data['refresh_token']
    context.uid = data['uid']
    
@then(u'o refresh_token do usuario é armazenado')
def step_armazenar_refresh_token(context):
    assert context.response.status_code in [200,201]
    data = context.response.json()
    assert data
    assert data['refresh_token']
    context.refresh_token = data['refresh_token']
    
@then(u'o uid do usuario é armazenado')
def step_armazenar_uid(context):
    assert context.response.status_code in [200,201]
    data = context.response.json()
    assert data
    assert data['uid']
    context.uid = data['uid']
    
@then(u'o sistema não retorna as informações de token do usuário')
def step_nao_retornar_tokens(context):
    data = context.response.json()
    assert data['message'] == 'Invalid username or password'
    assert context.response.status_code in [400,401]