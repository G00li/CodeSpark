import logging
import sys
import os
import json
from datetime import datetime
import traceback
from logging.handlers import RotatingFileHandler

# Configurações de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "logs/codespark_backend.log"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# Criar diretório de logs se não existir
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configurar o logger
def get_logger(name):
    logger = logging.getLogger(name)
    
    # Definir nível de log baseado na variável de ambiente
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Evitar duplicação de handlers
    if not logger.handlers:
        # Handler para console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)
        
        # Handler para arquivo com rotação
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=LOG_MAX_SIZE, backupCount=LOG_BACKUP_COUNT
        )
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)
    
    return logger

# Logger principal da aplicação
app_logger = get_logger("codespark.app")

# Classe para registrar logs de requisições e respostas
class RequestResponseLoggingMiddleware:
    async def __call__(self, request, call_next):
        # Log da requisição
        start_time = datetime.now()
        request_id = request.headers.get("X-Request-ID", str(start_time.timestamp()))
        
        # Preparar informações da requisição para logging
        request_info = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client_ip": request.client.host,
            "headers": dict(request.headers),
        }
        
        # Tentar obter o corpo da requisição
        try:
            body = await request.body()
            if body:
                request_info["body"] = body.decode()
        except Exception:
            request_info["body"] = "Could not read body"
        
        app_logger.info(f"Request received: {json.dumps(request_info)}")
        
        # Processar a requisição
        try:
            response = await call_next(request)
            
            # Log da resposta
            process_time = (datetime.now() - start_time).total_seconds()
            response_info = {
                "request_id": request_id,
                "status_code": response.status_code,
                "process_time_seconds": process_time,
                "headers": dict(response.headers),
            }
            
            app_logger.info(f"Response sent: {json.dumps(response_info)}")
            
            return response
        except Exception as e:
            # Log de erro
            error_info = {
                "request_id": request_id,
                "error": str(e),
                "traceback": traceback.format_exc(),
            }
            app_logger.error(f"Request failed: {json.dumps(error_info)}")
            raise

# Função para registrar logs de eventos específicos
def log_event(event_type, data, level="INFO"):
    """
    Registra um evento específico com dados adicionais
    
    Args:
        event_type: Tipo do evento (ex: 'user_created', 'project_generated')
        data: Dicionário com dados adicionais do evento
        level: Nível de log ('INFO', 'WARNING', 'ERROR', 'DEBUG')
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    event_data = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "data": data
    }
    
    event_logger = get_logger("codespark.events")
    event_logger.log(log_level, json.dumps(event_data))
    
    return event_data 