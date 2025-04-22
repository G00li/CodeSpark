import logging
from db_client import engine, Base
from models import User, Project, Task, ProjectType, TaskStatus

# Configurar o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas definidas.
    """
    logger.info("Criando tabelas do banco de dados...")
    try:
        # Criar tabelas
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas criadas com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {e}")
        raise

def test_connection():
    """
    Testa a conexão com o banco de dados.
    """
    from sqlalchemy import text
    
    logger.info("Testando conexão com o banco de dados...")
    try:
        # Criar uma conexão
        with engine.connect() as connection:
            # Executar uma consulta simples
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
            logger.info("Conexão com o banco de dados testada com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        raise

if __name__ == "__main__":
    # Testar a conexão primeiro
    test_connection()
    
    # Inicializar o banco de dados
    init_db() 