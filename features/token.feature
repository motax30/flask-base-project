Feature: Login do usuário na aplicação
    
Scenario: Usuário efetua a recuperação de seus tokens de autenticação 
    Given um usuário chamado user1
    and   o usuário possui uma senha 'pwd1'
    When  o usuário acessa o recurso para recuperação de suas informações de token
    Then  o acess_token do usuario é armazenado
    and   o refresh_token do usuario é armazenado
    and   o uid do usuario é armazenado

Scenario: Usuário informa uma senha incorreta ao recuperar o token
    Given um usuário chamado user1
    and   o usuário possui uma senha 'pwd4'
    When  o usuário acessa o recurso para recuperação de suas informações de token
    Then  o sistema não retorna as informações de token do usuário