from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import json
from db_client import Base

# Enums para compatibilidade com SQLAlchemy
class ProjectType(enum.Enum):
    BACKEND = "BACKEND"
    FRONTEND = "FRONTEND"
    FULLSTACK = "FULLSTACK"

class TaskStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    SKIPPED = "SKIPPED"

# Modelo de Usuário
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")

# Modelo de Projeto
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    project_type = Column(Enum(ProjectType), nullable=False)
    technologies = Column(Text, nullable=False)  # Armazenado como JSON
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    # Método para serializar/deserializar a lista de tecnologias
    @property
    def technologies_list(self):
        return json.loads(self.technologies)

    @technologies_list.setter
    def technologies_list(self, value):
        self.technologies = json.dumps(value)

# Modelo de Tarefa
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relacionamentos
    project = relationship("Project", back_populates="tasks") 