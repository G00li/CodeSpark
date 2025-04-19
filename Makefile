.PHONY: up down restart logs clean setup help

# Cores para mensagens
GREEN = \033[0;32m
BLUE = \033[0;34m
NC = \033[0m # No Color

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n",$$1,$$2}'


up: ## Start all containers
	@echo "${BLUE}Subindo containers...${NC}"
	docker compose up --build
	@echo "${GREEN}Todos os serviços estão rodando!${NC}"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "Documentação API: http://localhost:8000/docs"

down: ## Stop all containers
	@echo "${BLUE}Parando containers...${NC}"
	docker compose down
	@echo "${GREEN}Todos os serviços foram parados!${NC}"

restart: ## Restart all containers
	@echo "${BLUE}Reiniciando containers...${NC}"
	docker compose restart
	@echo "${GREEN}Todos os serviços foram reiniciados!${NC}"

logs: ## Show logs of all containers
	docker compose logs -f

clean: ## Clean all containers and volumes
	@echo "${BLUE}Limpando ambiente...${NC}"
	docker compose down -v --remove-orphans
	@echo "${GREEN}Ambiente limpo!${NC}"

setup: ## Setup environment variables
	@echo "${BLUE}Configurando ambiente de desenvolvimento...${NC}"
	@if [ ! -f .env ]; then \
		echo "Criando arquivo .env de exemplo..."; \
		echo "XATA_API_KEY=sua_xata_api_key_aqui" > .env; \
		echo "XATA_DATABASE_URL=https://seu-workspace-xata.io/db/seu-banco-de-dados" >> .env; \
		echo "OPENAI_API_KEY=sua_openai_api_key_aqui" >> .env; \
		echo "EXA_API_KEY=sua_exa_api_key_aqui" >> .env; \
	fi
	@echo "${GREEN}Ambiente configurado! Por favor, edite o arquivo .env com suas chaves de API.${NC}"
	@echo "Execute 'make up' para iniciar o projeto." 


logs_crewai: ## Show logs of CrewAi container
	@echo "${BLUE}Exibindo logs do container CrewAi...${NC}"
	docker logs -f codespark-crewai-1
	@echo "${GREEN}Logs do container CrewAi exibidos!${NC}"

logs_backend: ## Show logs of backend container
	@echo "${BLUE}Exibindo logs do container Backend...${NC}"
	docker logs -f codespark-backend-1
	@echo "${GREEN}Logs do container Backend exibidos!${NC}"

logs_frontend: ## Show logs of frontend container
	@echo "${BLUE}Exibindo logs do container Frontend...${NC}"
	docker logs -f codespark-frontend-1
	@echo "${GREEN}Logs do container Frontend exibidos!${NC}"
	
	
	
