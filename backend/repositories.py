from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from models import User, Project, Task, ProjectType, TaskStatus
import json
from datetime import datetime
from typing import List, Optional, Dict, Any

# Configurar o logger
logger = logging.getLogger(__name__)

# Base Repository para operações CRUD genéricas
class BaseRepository:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def get_by_id(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def list_all(self):
        return self.db.query(self.model).all()
    
    def create(self, data: Dict[str, Any]):
        try:
            db_item = self.model(**data)
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            return db_item
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erro ao criar {self.model.__name__}: {str(e)}")
            raise
    
    def update(self, id: int, data: Dict[str, Any]):
        try:
            db_item = self.get_by_id(id)
            if not db_item:
                return None
            
            for key, value in data.items():
                setattr(db_item, key, value)
            
            self.db.commit()
            self.db.refresh(db_item)
            return db_item
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erro ao atualizar {self.model.__name__}: {str(e)}")
            raise
    
    def delete(self, id: int):
        try:
            db_item = self.get_by_id(id)
            if not db_item:
                return False
            
            self.db.delete(db_item)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erro ao excluir {self.model.__name__}: {str(e)}")
            raise

# Repositório específico para usuários
class UserRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def get_with_projects(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

# Repositório específico para projetos
class ProjectRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Project)
    
    def get_by_owner(self, owner_id: int):
        return self.db.query(Project).filter(Project.owner_id == owner_id).all()
    
    def get_with_tasks(self, project_id: int):
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def create(self, data: Dict[str, Any]):
        # Processar a lista de tecnologias
        if 'technologies_list' in data:
            data['technologies'] = json.dumps(data.pop('technologies_list'))
        return super().create(data)
    
    def update(self, id: int, data: Dict[str, Any]):
        # Processar a lista de tecnologias
        if 'technologies_list' in data:
            data['technologies'] = json.dumps(data.pop('technologies_list'))
        return super().update(id, data)

# Repositório específico para tarefas
class TaskRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Task)
    
    def get_by_project(self, project_id: int):
        return self.db.query(Task).filter(Task.project_id == project_id).all()
    
    def complete_task(self, task_id: int):
        try:
            task = self.get_by_id(task_id)
            if not task:
                return None
            
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(task)
            return task
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erro ao completar tarefa: {str(e)}")
            raise 