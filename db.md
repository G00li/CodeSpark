# Migração do Xata.io para PostgreSQL

Este documento descreve a migração da base de dados do Xata.io para PostgreSQL no projeto CodeSpark.

## Motivação

Devido à incompatibilidade do Xata.io com Python, optamos por migrar para o PostgreSQL, uma solução de banco de dados relacional robusta, de código aberto e amplamente utilizada no mercado, com excelente suporte para aplicações Python.

## Estrutura Implementada

### 1. Container PostgreSQL

Foi criado um container Docker dedicado para o PostgreSQL:

- **Diretório**: `/workspaces/CodeSpark/db/`
- **Arquivos**:
  - `Dockerfile`: Configuração do container PostgreSQL
  - `init.sql`: Script SQL para inicialização do banco de dados com as tabelas necessárias

### 2. Modelagem de Dados

A modelagem de dados foi implementada usando SQLAlchemy:

- **Arquivo**: `/workspaces/CodeSpark/backend/models.py`
- **Modelos implementados**:
  - `User`: Usuários do sistema
  - `Project`: Projetos gerenciados pelo sistema
  - `Task`: Tarefas associadas aos projetos

### 3. Integração com a Aplicação

A integração com o backend foi realizada através de:

- **Arquivo de conexão**: `/workspaces/CodeSpark/backend/db_client.py`
- **Repositórios CRUD**: `/workspaces/CodeSpark/backend/repositories.py`

### 4. Migração de Dados

Para gerenciar as migrações de banco de dados, foi implementado o Alembic:

- **Diretório de migrações**: `/workspaces/CodeSpark/backend/migrations/`
- **Arquivos de configuração**:
  - `alembic.ini`: Configuração principal do Alembic
  - `migrations/env.py`: Ambiente de migração
  - `migrations/script.py.mako`: Template para scripts de migração

## Modificações no docker-compose.yaml

O arquivo `docker-compose.yaml` foi atualizado para:

1. Adicionar o serviço PostgreSQL
2. Atualizar o serviço backend para se conectar ao PostgreSQL
3. Adicionar volumes para persistência de dados

## Testes e Validação

Para testar a conectividade com o banco de dados e inicializar a estrutura, foi criado o script:

- **Arquivo**: `/workspaces/CodeSpark/backend/init_db.py`

Este script realiza:
1. Teste de conexão com o banco de dados
2. Criação das tabelas definidas nos modelos

## Como Executar

Para iniciar o ambiente com a nova configuração de banco de dados:

```bash
# Na raiz do projeto
docker-compose up --build
```

Para executar apenas o teste de conexão e inicialização do banco:

```bash
# No diretório backend
python init_db.py
```

Para criar uma nova migração após alterações nos modelos:

```bash
# No diretório backend
alembic revision --autogenerate -m "Descrição da migração"
```

Para aplicar migrações pendentes:

```bash
# No diretório backend
alembic upgrade head
```

## Comparação com Xata.io

### Vantagens da Migração

1. **Melhor compatibilidade**: PostgreSQL tem suporte nativo e robusto para Python
2. **Controle local**: Banco de dados executado em container, facilitando desenvolvimento e testes
3. **Escalabilidade**: PostgreSQL oferece excelente desempenho mesmo com grandes volumes de dados
4. **Flexibilidade**: SQLAlchemy permite modelagem de dados avançada e consultas complexas
5. **Comunidade e suporte**: Ampla documentação e comunidade ativa

### Mudanças na Arquitetura

1. Substituição do cliente Xata pelo SQLAlchemy + psycopg2
2. Implementação de padrão Repository para operações CRUD
3. Adição de sistema de migração com Alembic
4. Inclusão de container dedicado para banco de dados

## Próximos Passos

1. Implementar camada de serviços para lógica de negócios
2. Adicionar testes automatizados para o acesso ao banco de dados
3. Configurar backup automatizado do banco de dados
4. Implementar índices adicionais para otimização de consultas frequentes 