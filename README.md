# mini-twitter
Mini-twitter é um projeto que consiste em um minissistema que implementa, em python, algumas das funcionalidades principais do Twitter.

# guia de instalação do projeto

# Docker
1. Faça download do projeto
2. No diretório do projeto digite o comando:
```sh
docker-compose up -d
```

# Windows
1. Faça download do projeto
2. No diretório do projeto digite os comandos:
```sh 
python -m venv venv
```

```sh 
.\venv\scripts\activate
```

```sh 
pip install -r requirements.txt
```
```sh 
python manage.py runserver 
```


# Linux/MacOs
1. Faça download do projeto
2. No diretório do projeto digite os comandos:

```sh 
python3 -m venv venv
```
```sh 
source venv/bin/activate
```
```sh 
pip install -r requirements.txt
```
```sh 
python3 manage.py runserver
```
# Credenciais de super usuário
1. username: admin
2. email: admin@gmail.com
3. password: 123

# Documentação da API
## User

### Listar Usuários

#### Retorna uma lista de todos os usuários.

#### URL: api/user/

#### Método: GET

#### Resposta:

<pre>
[
    {
        "id": 1,
        "username": "john.doe",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    },
    {
        "id": 2,
        "username": "jane.doe",
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    },
    ...
]

</pre>

### Criar Usuário

#### Cria um novo usuário.

#### URL: api/user/create_user/

#### Método: POST

#### Corpo da Requisição:

<pre>
{
    "username": "novousuario",
    "first_name": "Novo",
    "last_name": "Usuário",
    "email": "novousuario@example.com",
    "password": "senha123"
}
</pre>

#### Resposta:

<pre>
{
    "message": "Usuário criado!",
    "id": 3,
    "username": "novousuario",
    "first_name": "Novo",
    "last_name": "Usuário",
    "email": "novousuario@example.com"
}
</pre>

## Login

### Fazer login no sistema
#### URL: api/token/

#### Método: POST

#### Corpo da requisição:
<pre>
{
	"username":"jhon.doe",
	"password": "senha123"
}
</pre>

#### Resposta:
<pre>
{
	"refresh": "refresh token",
	"access": "access token"
}
</pre>

## Perfil

### Obter Perfil do Usuário
#### Recupera o perfil de um usuário.

#### URL: api/profile/get_profile/?user_id=id

#### Método: GET

#### Resposta:

<pre>
{
    "id": 1,
    "photo": "http://example.com/caminho/para/foto.jpg",
    "user": {
        "id": 1,
        "username": "john.doe",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    },
    "created_at": "2023-05-24T12:00:00Z"
}
</pre>

### Criar Perfil do Usuário
#### Cria um perfil para um usuário.

#### URL: api/profile/register_profile/

#### Método: POST

#### Corpo da Requisição:

<pre>
{
    "user_id": 1,
    "profile_image": "http://example.com/caminho/para/imagem_de_perfil.jpg"
}
</pre>

#### Resposta:

<pre>
{
    "message": "Perfil criado!",
    "id": 1,
    "photo": "http://example.com/caminho/para/foto.jpg",
    "user": {
        "id": 1,
        "username": "john.doe",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    },
    "created_at": "2023-05-24T12:00:00Z"
}
</pre>

### Adicionar Seguidor
#### Adiciona um seguidor a um usuário.

#### URL: api/profile/add_follower/

#### Método: POST

#### Corpo da Requisição:

<pre>
{
    "user_id": 1,
    "follower_id": 2
}
</pre>

#### Resposta:

<pre>
{
    "message": "Seguidor adicionado com sucesso"
}
</pre>

## Posts
### Obter Meus Posts
#### Recupera as publicações de um usuário.

#### URL: api/posts/get_my_posts/?user_id=id

#### Método: GET

#### Resposta:

<pre>
[
    {
        "id": 1,
        "user": {
            "id": 1,
            "username": "john.doe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        },
        "twitt": "Minha primeira postagem",
        "created_at": "2023-05-24T12:00:00Z",
        "photo": "http://example.com/caminho/para/foto1.jpg"
    },
    {
        "id": 2,
        "user": {
            "id": 1,
            "username": "john.doe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        },
        "twitt": "Minha segunda postagem",
        "created_at": "2023-05-25T12:00:00Z",
        "photo": "http://example.com/caminho/para/foto2.jpg"
    },
    ...
]

</pre>


### Obter Feed Geral
#### Recupera as publicações dos usuários.

#### URL: api/posts/

#### Método: GET

#### Resposta:

<pre>
[
    {
        "id": 1,
        "user": {
            "id": 2,
            "username": "jane.doe",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        },
        "twitt": "Postagem da Jane",
        "created_at": "2023-05-24T12:00:00Z",
        "photo": "http://example.com/caminho/para/foto3.jpg"
    },
    {
        "id": 2,
        "user": {
            "id": 3,
            "username": "novousuario",
            "first_name": "Novo",
            "last_name": "Usuário",
            "email": "novousuario@example.com"
        },
        "twitt": "Postagem do Novo Usuário",
        "created_at": "2023-05-25T12:00:00Z",
        "photo": "http://example.com/caminho/para/foto4.jpg"
    },
    ...
]

</pre>

### Obter Feed Personalizado
#### Recupera as publicações dos usuários seguidos por um usuário.

#### URL: api/posts/get_followers_posts/?user_id=id

#### Método: GET

#### Resposta:
<pre>
[
    {
        "id": 1,
        "user": {
            "id": 2,
            "username": "jane.doe",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        },
        "twitt": "Postagem da Jane",
        "created_at": "2023-05-24T12:00:00Z",
        "photo": "http://example.com/caminho/para/foto3.jpg"
    },
    {
        "id": 2,
        "user": {
            "id": 3,
            "username": "novousuario",
            "first_name": "Novo",
            "last_name": "Usuário",
            "email": "novousuario@example.com"
        },
        "twitt": "Postagem do Novo Usuário",
        "created_at": "2023-05-25T12:00:00Z",
        "photo": "http://example.com/caminho/para/foto4.jpg"
    },
    ...
]

</pre>

### Criar Publicação
#### Cria uma nova publicação.

#### URL: /posts/register_publication/

#### Método: POST

#### Corpo da Requisição:

<pre>
{
    "user_id": 1,
    "twitt": "Minha nova postagem",
    "photo": "http://example.com/caminho/para/foto.jpg"
}

</pre>

#### Resposta:

<pre>
{
    "message": "Publicação criada!",
    "id": 3,
    "user": {
        "id": 1,
        "username": "john.doe",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    },
    "twitt": "Minha nova postagem",
    "created_at": "2023-05-24T12:00:00Z",
    "photo": "http://example.com/caminho/para/foto.jpg"
}

</pre>
