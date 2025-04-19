import os
from contextlib import contextmanager
from dotenv import load_dotenv
from xata.client import XataClient

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do cliente Xata
XATA_API_KEY = os.getenv("XATA_API_KEY")
XATA_DATABASE_URL = os.getenv("XATA_DATABASE_URL")

if not XATA_API_KEY or not XATA_DATABASE_URL:
    raise ValueError("As variáveis de ambiente XATA_API_KEY e XATA_DATABASE_URL são obrigatórias")

# Função para obter cliente Xata
@contextmanager
def get_xata_client():
    client = XataClient(
        api_key=XATA_API_KEY,
        db_url=XATA_DATABASE_URL
    )
    try:
        yield client
    finally:
        # O cliente Xata não tem um método de desconexão explícito
        pass

# Função para utilizar como dependência no FastAPI
def get_db():
    with get_xata_client() as xata:
        yield xata 