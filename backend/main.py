from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import httpx
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# Caminho do projeto raiz
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(PROJECT_ROOT, '.env')

# Carregar variáveis de ambiente da raiz
load_dotenv(dotenv_path=ENV_PATH)

# Importar dependência do cliente do banco de dados
from db_client import get_db, engine, Base
import schemas
from routers import users, projects, tasks
from logger import get_logger, RequestResponseLoggingMiddleware, log_event
from models import User, Project, Task  # Importar modelos SQLAlchemy

# Criar logger para aplicação principal
logger = get_logger(__name__)

# Inicializar banco de dados
Base.metadata.create_all(bind=engine)

# Criar aplicação FastAPI
app = FastAPI(title="CodeSpark API", 
              description="API para o CodeSpark, uma plataforma de desenvolvimento de projetos guiada por IA")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar middleware de logging
app.add_middleware(RequestResponseLoggingMiddleware)

# Incluir routers
app.include_router(users.router, prefix="/api/users", tags=["Usuários"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projetos"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tarefas"])

@app.get("/")
def read_root():
    logger.info("Endpoint raiz acessado")
    return {"message": "Bem-vindo à API do CodeSpark!"}

@app.get("/health")
def health_check():
    logger.info("Verificação de saúde realizada")
    return {"status": "healthy"}

@app.post("/api/generate-project", response_model=schemas.ProjectProposal)
async def generate_project(
    request: schemas.ProjectRequest,
    db: Session = Depends(get_db)
):
    """
    Gera uma proposta de projeto baseada nas tecnologias e tipo de projeto solicitados.
    Utiliza o serviço CrewAI para criar uma proposta detalhada.
    """
    try:
        logger.info(f"Solicitação de geração de projeto recebida: {request.dict()}")
        
        # Chamada para o serviço CrewAI
        async with httpx.AsyncClient(timeout=60.0) as client:
            logger.debug(f"Enviando solicitação para o serviço CrewAI")
            response = await client.post(
                "http://crewai:8001/generate",
                json={
                    "project_type": request.project_type.value,
                    "technologies": request.technologies,
                    "additional_info": request.additional_info
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Erro ao gerar proposta de projeto: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao gerar proposta de projeto"
                )
            
            result = response.json()
            log_event("project_proposal_generated", {"project_type": request.project_type.value, "technologies": request.technologies})
            logger.info(f"Proposta de projeto gerada com sucesso: {result.get('title')}")
            return result
    except Exception as e:
        logger.exception(f"Exceção ao comunicar com o serviço CrewAI: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao comunicar com o serviço CrewAI: {str(e)}"
        ) 