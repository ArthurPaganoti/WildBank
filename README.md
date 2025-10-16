# WildBank API

Este projeto é uma API REST.

## Pré-requisitos
- Docker
- Docker Compose
- Python 3.10+
- (Opcional) Banco de dados PostgreSQL

## Como rodar o backend
1. Clone o repositório e acesse a pasta do projeto.
2. Configure as variáveis de ambiente necessárias em um arquivo `.env` na raiz do projeto. Use o arquivo `.env.example` como base:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env conforme necessário
   ```
3. Para rodar com Docker Compose:
   ```bash
   docker compose up -d
   ```
   Ou utilize o script shell para facilitar:
   ```bash
   ./docker-start.sh
   ```

## Como rodar o front-end
1. Acesse a pasta `frontend`:
   ```bash
   cd frontend
   ```
2. Instale as dependências:
   ```bash
   npm install
   ```
3. Inicie o front-end em modo desenvolvimento:
   ```bash
   npm run dev
   ```
   O front-end estará disponível em `http://localhost:5173` por padrão.

## Endpoints principais

### POST `/users/login`
Autentica um usuário.
**Exemplo de requisição:**
```json
{
  "email": "usuario@email.com",
  "senha": "minhasenha123"
}
```

### POST `/users/refresh`
Renova o token de autenticação.
**Exemplo de requisição:**
```json
{
  "refresh_token": "token_aqui"
}
```

### POST `/users/logout`
Faz logout do usuário autenticado.

### POST `/users/`
Cadastra um novo usuário.
**Exemplo de requisição:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "senhaSegura123"
}
```

### GET `/users/`
Lista usuários (público, limitado a 100 por página).

### GET `/users/me`
Retorna os dados do usuário autenticado.

### GET `/users/get/nome/{nome}`
Busca usuários pelo nome.

### GET `/users/get/email/{email}`
Busca usuário pelo e-mail.

### DELETE `/users/{user_id}`
Remove um usuário pelo ID.

### PUT `/users/{user_id}`
Atualiza e-mail e senha do usuário.
**Exemplo de requisição:**
```json
{
  "email": "novo@email.com",
  "senha": "novaSenha123"
}
```

### POST `/users/password-reset/request`
Solicita redefinição de senha.
**Exemplo de requisição:**
```json
{
  "email": "usuario@email.com"
}
```

### POST `/users/password-reset/confirm`
Confirma redefinição de senha.
**Exemplo de requisição:**
```json
{
  "token": "token_recebido",
  "new_password": "novaSenha123"
}
```
