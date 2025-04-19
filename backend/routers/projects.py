from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from xata.client import XataClient

import schemas
from xata_client import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.ProjectCreate, user_id: str, db: XataClient = Depends(get_db)):
    # Verificar se o usuário existe
    user_record = db.records().get("users", user_id)
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Criar o projeto com Xata
    project_data = {
        "title": project.title,
        "description": project.description,
        "projectType": project.projectType.value,
        "technologies": project.technologies,
        "ownerId": user_id,
        "isActive": True
    }
    
    result = db.records().insert("projects", project_data)
    
    # Adaptar o resultado para o formato esperado
    return {
        "id": result["id"],
        "title": result["title"],
        "description": result["description"],
        "projectType": result["projectType"],
        "technologies": result["technologies"],
        "ownerId": result["ownerId"],
        "isActive": result["isActive"],
        "createdAt": result["xata"]["createdAt"]
    }

@router.get("/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: XataClient = Depends(get_db)):
    response = db.data().query("projects", {
        "page": {
            "size": limit,
            "offset": skip
        }
    })
    
    projects = []
    for record in response["records"]:
        projects.append({
            "id": record["id"],
            "title": record["title"],
            "description": record["description"],
            "projectType": record["projectType"],
            "technologies": record["technologies"],
            "ownerId": record["ownerId"],
            "isActive": record.get("isActive", True),
            "createdAt": record["xata"]["createdAt"]
        })
    
    return projects

@router.get("/{project_id}", response_model=schemas.ProjectWithTasks)
def read_project(project_id: str, db: XataClient = Depends(get_db)):
    # Buscar projeto
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
    for task in tasks_response.get("records", []):
        tasks.append({
            "id": task["id"],
            "title": task["title"],
            "description": task["description"],
            "status": task["status"],
            "projectId": task["projectId"],
            "createdAt": task["xata"]["createdAt"],
            "completedAt": task.get("completedAt")
        })
    
    # Construir resposta
    return {
        "id": project_record["id"],
        "title": project_record["title"],
        "description": project_record["description"],
        "projectType": project_record["projectType"],
        "technologies": project_record["technologies"],
        "ownerId": project_record["ownerId"],
        "isActive": project_record.get("isActive", True),
        "createdAt": project_record["xata"]["createdAt"],
        "tasks": tasks
    }

@router.get("/user/{user_id}", response_model=List[schemas.Project])
def read_user_projects(user_id: str, db: XataClient = Depends(get_db)):
    # Verificar se o usuário existe
    user_record = db.records().get("users", user_id)
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Buscar projetos do usuário
    projects_response = db.data().query("projects", {
        "filter": {
            "ownerId": user_id
        }
    })
    
    projects = []
    for record in projects_response.get("records", []):
        projects.append({
            "id": record["id"],
            "title": record["title"],
            "description": record["description"],
            "projectType": record["projectType"],
            "technologies": record["technologies"],
            "ownerId": record["ownerId"],
            "isActive": record.get("isActive", True),
            "createdAt": record["xata"]["createdAt"]
        })
    
    return projects 