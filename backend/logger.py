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
    def __init__(self, app):
        self.app = app
        
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
            
        # Criar um contexto de requisição
        request_id = None
        start_time = datetime.now()
        
        # Função para interceptar a resposta
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # Log da resposta
                process_time = (datetime.now() - start_time).total_seconds()
                
                # Converter headers se existirem
                response_headers = {}
                if "headers" in message:
                    for key, value in message["headers"]:
                        response_headers[key.decode("utf-8")] = value.decode("utf-8")
                
                response_info = {
                    "request_id": request_id,
                    "status_code": message["status"],
                    "process_time_seconds": process_time,
                    "headers": response_headers,
                }
                
                app_logger.info(f"Response sent: {json.dumps(response_info)}")
                
            await send(message)
        
        # Log da requisição
        if scope["type"] == "http":
            path = scope.get("path", "")
            method = scope.get("method", "")
            
            # Converter headers de lista de tuplas (bytes, bytes) para dicionário de strings
            raw_headers = scope.get("headers", [])
            headers = {}
            for key, value in raw_headers:
                headers[key.decode("utf-8")] = value.decode("utf-8")
                
            client = scope.get("client", ("unknown", 0))
            
            request_id = str(datetime.now().timestamp())
            
            # Preparar informações da requisição para logging
            request_info = {
                "request_id": request_id,
                "method": method,
                "path": path,
                "client_ip": f"{client[0]}:{client[1]}",
                "headers": headers,
            }
            
            app_logger.info(f"Request received: {json.dumps(request_info)}")
        
        # Processar a requisição
        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            # Log de erro
            error_info = {
                "request_id": request_id,
                "path": scope.get("path", ""),
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