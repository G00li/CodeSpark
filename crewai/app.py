import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import asyncio
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

from crew_manager import generate_project_proposal

app = FastAPI(title="CodeSpark CrewAI Service",
              description="Serviço de IA para o CodeSpark, utilizando CrewAI para gerar propostas de projeto")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProjectRequest(BaseModel):
    project_type: str
    technologies: List[str]
    additional_info: Optional[str] = None

class ProjectTask(BaseModel):
    title: str
    description: str

class ProjectResponse(BaseModel):
    title: str
    description: str
    goals: List[str]
    tasks: List[ProjectTask]
    technologies: List[str]

@app.get("/")
async def read_root():
    return {"message": "Bem-vindo ao serviço CrewAI do CodeSpark!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Utilizando ProcessPoolExecutor para processamento paralelo
executor = ProcessPoolExecutor(max_workers=4)

@app.post("/generate", response_model=ProjectResponse)
async def generate_project(request: ProjectRequest):
    """
    Gera uma proposta de projeto baseada no tipo de projeto e tecnologias especificadas.
    """
    try:
        # Executando a geração do projeto em um processo separado para não bloquear
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            generate_project_proposal,
            request.project_type,
            request.technologies,
            request.additional_info
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar proposta: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True) 