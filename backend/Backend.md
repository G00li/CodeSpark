# CodeSpark Backend

Este é o backend do projeto CodeSpark, uma plataforma para criação de trilhas de aprendizado de programação guiadas por IA.

## Tecnologias utilizadas

- FastAPI
- Xata.io (Banco de dados serverless)
- Redis
- Python 3.11
- CrewAI

## Configuração do ambiente

### Requisitos

- Python 3.11+
- Conta no Xata.io para o banco de dados
- Chave de API do OpenAI para o CrewAI

### Instalação

1. Instale as dependências Python:

```bash
pip install -r requirements.txt
```

2. Crie um arquivo `.env` na pasta backend com as seguintes variáveis:

```bash
# Configurações do Xata.io
XATA_API_KEY=sua_xata_api_key_aqui
XATA_DATABASE_URL=https://seu-workspace-xata.io/db/seu-banco-de-dados

# Chave da API OpenAI para o CrewAI
OPENAI_API_KEY=sua_openai_api_key_aqui
```

3. Configure seu banco de dados no Xata.io:

   - Crie uma conta em https://xata.io/
   - Crie um novo banco de dados
   - Configure as tabelas:
     - users (email, name, hashedPassword, isActive)
     - projects (title, description, projectType, technologies, ownerId, isActive)
     - tasks (title, description, status, projectId, completedAt)

### Executando o servidor

```bash
uvicorn main:app --reload
```

O servidor estará disponível em http://localhost:8000.

## Estrutura do projeto

- `main.py`: Ponto de entrada da aplicação FastAPI
- `xata_client.py`: Cliente Xata.io para conexão com o banco de dados
- `schemas.py`: Modelos Pydantic para validação de dados
- `routers/`: Rotas da API

## Funcionamento do projeto

O CodeSpark é uma plataforma que permite aos usuários:

1. **Criar uma conta e fazer login** (via NextAuth no frontend)
2. **Gerar propostas de projetos** personalizadas com base em:
   - Tipo de projeto (Backend, Frontend, Fullstack)
   - Tecnologias desejadas
   - Informações adicionais (opcional)
3. **Acompanhar o progresso** em uma trilha de tarefas
4. **Marcar tarefas como concluídas**

O fluxo principal funciona da seguinte forma:

1. O usuário seleciona as tecnologias e o tipo de projeto
2. A API chama o serviço CrewAI, que utiliza LLMs para gerar uma proposta de projeto
3. A proposta inclui título, descrição, objetivos e tarefas
4. O usuário aceita a proposta, criando um novo projeto
5. O usuário acompanha o progresso marcando as tarefas como concluídas

## Docker

O projeto inclui configurações Docker para facilitar o desenvolvimento e implantação. Para executar com Docker:

```bash
docker-compose up
```

Isso inicializará todos os serviços necessários:
- Frontend (Next.js)
- Backend (FastAPI)
- CrewAI (Serviço de IA)
- Redis (Cache)

## Autenticação

A autenticação dos usuários é gerenciada pelo NextAuth no frontend. O backend recebe apenas requisições com tokens validados. 