Feature: Gerenciar usuários

Scenario: Listar um usuário cadastrado informando o token de autenticação
    Given um usuário chamado user1
    and   o usuário possui uma senha 'pwd1'
    and   o usuário possui as informações de token e uid
    When  consultadas as informações do usuario 'user1'
    Then  as informações do usuário 'user1' serão retornadas.

Scenario: Listar um usuário cadastrado sem informar o token de autenticação
    Given um usuário chamado user1
    and   o usuário possui uma senha 'pwd1'
    When  consultadas as informações do usuario 'user1' sem informar o token
    Then  as informações do usuário 'user1' não serão retornadas.

Scenario: Cadastrar um novo usuario
    Given um usuário chamado 'adriano'
    and   o usuário possui uma senha 'pwd1'
    When  o usuário acessa o recurso para cadatrar o usuario
    Then  o usuario 'adriano' é cadatrado com sucesso 

Scenario: Não informar usuario e senha para cadastro de um novo usuario
    When  o usuário acessa o recurso para cadatrar o usuario
    Then  o sistema retorna um erro de processamento