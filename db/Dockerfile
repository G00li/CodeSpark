FROM postgres:15-alpine

# Variáveis de ambiente para criação do banco
ENV POSTGRES_DB=codespark
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Copiar scripts de inicialização
COPY ./init.sql /docker-entrypoint-initdb.d/

# Expor a porta do PostgreSQL
EXPOSE 5432 