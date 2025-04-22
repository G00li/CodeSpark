from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Adicionar o diretório pai ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importações do projeto
from db_client import Base, DATABASE_URL
import models

# Alembic Config
config = context.config

# Sobrescrever a URL de conexão com a do projeto
config.set_main_option('sqlalchemy.url', DATABASE_URL)

# Interpretação dos arquivos de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados para 'autogenerate'
target_metadata = Base.metadata

def run_migrations_offline():
    """
    Executa migrações em modo 'offline'.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """
    Executa migrações em modo 'online'.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online() 