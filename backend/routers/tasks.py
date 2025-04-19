from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from xata.client import XataClient
from datetime import datetime

import schemas
from xata_client import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: XataClient = Depends(get_db)):
    # Verificar se o projeto existe
    project_record = db.records().get("projects", task.projectId)
    if not project_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    # Criar a tarefa com Xata
    task_data = {
        "title": task.title,
        "description": task.description,
        "projectId": task.projectId,
        "status": schemas.TaskStatus.PENDING.value
    }
    
    result = db.records().insert("tasks", task_data)
    
    # Adaptar o resultado para o formato esperado
    return {
        "id": result["id"],
        "title": result["title"],
        "description": result["description"],
        "status": result["status"],
        "projectId": result["projectId"],
        "createdAt": result["xata"]["createdAt"],
        "completedAt": None
    }

@router.get("/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: XataClient = Depends(get_db)):
    response = db.data().query("tasks", {
        "page": {
            "size": limit,
            "offset": skip
        }
    })
    
    tasks = []
    for record in response["records"]:
        tasks.append({
            "id": record["id"],
            "title": record["title"],
            "description": record["description"],
            "status": record["status"],
            "projectId": record["projectId"],
            "createdAt": record["xata"]["createdAt"],
            "completedAt": record.get("completedAt")
        })
    
    return tasks

@router.get("/{task_id}", response_model=schemas.Task)
def read_task(task_id: str, db: XataClient = Depends(get_db)):
    task_record = db.records().get("tasks", task_id)
    if not task_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    # Adaptar o resultado para o formato esperado
    return {
        "id": task_record["id"],
        "title": task_record["title"],
        "description": task_record["description"],
        "status": task_record["status"],
        "projectId": task_record["projectId"],
        "createdAt": task_record["xata"]["createdAt"],
        "completedAt": task_record.get("completedAt")
    }

@router.put("/{task_id}", response_model=schemas.Task)
def update_task_status(task_id: str, task_update: schemas.TaskUpdate, db: XataClient = Depends(get_db)):
    # Verificar se a tarefa existe
    task_record = db.records().get("tasks", task_id)
    if not task_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    # Preparar dados de atualização
    update_data = {"status": task_update.status.value}
    
    # Se o status for COMPLETED, adicionar a data de conclusão
    if task_update.status == schemas.TaskStatus.COMPLETED:
        update_data["completedAt"] = datetime.now().isoformat()
    
    # Atualizar a tarefa
    result = db.records().update("tasks", task_id, update_data)
    
    # Adaptar o resultado para o formato esperado
    return {
        "id": result["id"],
        "title": result["title"],
        "description": result["description"],
        "status": result["status"],
        "projectId": result["projectId"],
        "createdAt": result["xata"]["createdAt"],
        "completedAt": result.get("completedAt")
    }

@router.get("/project/{project_id}", response_model=List[schemas.Task])
def read_project_tasks(project_id: str, db: XataClient = Depends(get_db)):
    # Verificar se o projeto existe
    project_record = db.records().get("projects", project_id)
    if not project_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    # Buscar tarefas do projeto
    tasks_response = db.data().query("tasks", {
        "filter": {
            "projectId": project_id
        }
    })
    
    tasks = []
    for record in tasks_response.get("records", []):
        tasks.append({
            "id": record["id"],
            "title": record["title"],
            "description": record["description"],
            "status": record["status"],
            "projectId": record["projectId"],
            "createdAt": record["xata"]["createdAt"],
            "completedAt": record.get("completedAt")
        })
    
    return tasks 