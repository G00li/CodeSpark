import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Caminho do projeto raiz (um nível acima do diretório atual)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(PROJECT_ROOT, '.env')

# Carregar variáveis de ambiente do arquivo .env na raiz
load_dotenv(dotenv_path=ENV_PATH)

# Configurar conexão com o PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/codespark")

# Criar engine do SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos ORM
Base = declarative_base()

@contextmanager
def get_db_session():
    """
    Contexto para gerenciar sessões do banco de dados,
    garantindo que a sessão seja fechada após o uso.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Função para utilizar como dependência no FastAPI
def get_db():
    """
    Dependência para injetar uma sessão do banco de dados
    em rotas do FastAPI.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close() 