from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from passlib.context import CryptContext
from xata.client import XataClient

import schemas
from xata_client import get_db

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: XataClient = Depends(get_db)):
    # Verificar se o e-mail já está em uso
    existing_user = db.data().query("users", {
        "filter": {
            "email": user.email
        }
    })
    
    if existing_user and existing_user["records"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso"
        )
    
    hashed_password = get_password_hash(user.password)
    
    # Criar o usuário com Xata
    user_data = {
        "email": user.email,
        "name": user.name,
        "hashedPassword": hashed_password,
        "isActive": True
    }
    
    result = db.records().insert("users", user_data)
    
    # Adaptar o resultado para o formato esperado pelo schema
    return {
        "id": result["id"],
        "email": result["email"],
        "name": result["name"],
        "isActive": result["isActive"],
        "createdAt": result["xata"]["createdAt"]
    }

@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: XataClient = Depends(get_db)):
    response = db.data().query("users", {
        "page": {
            "size": limit,
            "offset": skip
        }
    })
    
    users = []
    for record in response["records"]:
        users.append({
            "id": record["id"],
            "email": record["email"],
            "name": record["name"],
            "isActive": record.get("isActive", True),
            "createdAt": record["xata"]["createdAt"]
        })
    
    return users

@router.get("/{user_id}", response_model=schemas.UserWithProjects)
def read_user(user_id: str, db: XataClient = Depends(get_db)):
    # Buscar usuário
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
    for project in projects_response.get("records", []):
        projects.append({
            "id": project["id"],
            "title": project["title"],
            "description": project["description"],
            "projectType": project["projectType"],
            "technologies": project["technologies"],
            "ownerId": project["ownerId"],
            "isActive": project.get("isActive", True),
            "createdAt": project["xata"]["createdAt"]
        })
    
    # Construir resposta
    return {
        "id": user_record["id"],
        "email": user_record["email"],
        "name": user_record["name"],
        "isActive": user_record.get("isActive", True),
        "createdAt": user_record["xata"]["createdAt"],
        "projects": projects
    } 