from behave import *
import json
import requests

@given(u'o usuário possui as informações de token e uid')
def step_impl(context):
    user_data={'password': context.password,'username': context.username}
    headers={'content-type': 'application/json'}
    context.response  = requests.post("http://localhost:5000/token", data=json.dumps(user_data), headers=headers)
    assert context.response.status_code in [200,201]
    data = context.response.json()
    assert data
    assert data['access_token']
    context.acess_token = data['access_token']
    assert data['uid']
    context.uid = data['uid']

@when(u'consultadas as informações do usuario \'user1\'')
def step_impl(context):
    user_data={'uid': str(context.uid)}
    headers = {
        'Authorization': 'Bearer '+ str(context.acess_token),
    }
    context.response = requests.get("http://localhost:5000/user", params=user_data, headers=headers)
    assert context.response.status_code in [200,201]

@when(u'consultadas as informações do usuario \'user1\' sem informar o token' )
def step_impl(context):
    context.response = requests.get("http://localhost:5000/user")
    assert context.response.status_code in [400,401,422]

@then(u'as informações do usuário \'user1\' serão retornadas.')
def step_impl(context):
    data = context.response.json()
    assert data
    assert data['id']
    assert data['username']

@then(u'as informações do usuário \'user1\' não serão retornadas.')
def step_impl(context):
    assert context.response.status_code in [400,401,422]

@when(u'o usuário acessa o recurso para cadatrar o usuario')
def step_impl(context):
    user_data={'password': 'senha_teste','username': 'novo_usuario'}
    headers={'content-type': 'application/json'}
    context.response  = requests.post("http://localhost:5000/user", data=json.dumps(user_data), headers=headers)
    assert context.response.status_code in [200]