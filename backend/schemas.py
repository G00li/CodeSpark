from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

# Definição de enums para compatibilidade com Xata
class ProjectType(str, Enum):
    BACKEND = "BACKEND"
    FRONTEND = "FRONTEND"
    FULLSTACK = "FULLSTACK"

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    SKIPPED = "SKIPPED"

# Schemas para usuários
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str  # Xata usa string como ID
    isActive: bool
    createdAt: datetime

    class Config:
        orm_mode = True
        from_attributes = True

# Schemas para criação e resposta de projetos
class ProjectRequest(BaseModel):
    project_type: ProjectType
    technologies: List[str]
    additional_info: Optional[str] = None

class ProjectTask(BaseModel):
    title: str
    description: str

class ProjectProposal(BaseModel):
    title: str
    description: str
    goals: List[str]
    tasks: List[ProjectTask]
    technologies: List[str]

class ProjectBase(BaseModel):
    title: str
    description: str
    projectType: ProjectType
    technologies: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str  # Xata usa string como ID
    ownerId: str  # Referência a outro registro com ID string
    isActive: bool
    createdAt: datetime
    
    class Config:
        orm_mode = True
        from_attributes = True

# Schemas para tarefas
class TaskBase(BaseModel):
    title: str
    description: str

class TaskCreate(TaskBase):
    projectId: str  # Referência ao projeto com ID string

class TaskUpdate(BaseModel):
    status: TaskStatus

class Task(TaskBase):
    id: str  # Xata usa string como ID
    status: TaskStatus
    projectId: str  # Referência ao projeto com ID string
    createdAt: datetime
    completedAt: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        from_attributes = True

# Schemas para relacionamentos
class ProjectWithTasks(Project):
    tasks: List[Task] = []
    
    class Config:
        orm_mode = True
        from_attributes = True

class UserWithProjects(User):
    projects: List[Project] = []
    
    class Config:
        orm_mode = True
        from_attributes = True 