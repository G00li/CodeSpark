from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from typing import List, Dict, Any, Optional
import os

# Configuração do modelo de linguagem
llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0.5,
)

def generate_project_proposal(project_type: str, technologies: List[str], additional_info: Optional[str] = None) -> Dict[str, Any]:
    """
    Gera uma proposta de projeto utilizando CrewAI.
    
    Args:
        project_type: Tipo de projeto (backend, frontend, fullstack)
        technologies: Lista de tecnologias a serem utilizadas
        additional_info: Informações adicionais sobre o projeto
        
    Returns:
        Proposta de projeto formatada
    """
    
    # Definição de agentes especializados
    project_manager = Agent(
        role="Gerente de Projeto",
        goal="Coordenar e garantir que o projeto seja bem definido, prático e desafiador",
        backstory="""Você é um experiente gerente de projetos de software com anos de experiência 
        em desenvolvimento de produtos digitais. Sua função é garantir que o projeto seja 
        bem estruturado, com escopo definido e metas claras.""",
        verbose=True,
        llm=llm,
    )
    
    tech_specialist = Agent(
        role="Especialista em Tecnologia",
        goal="Garantir que as tecnologias solicitadas sejam utilizadas de forma eficiente e coerente",
        backstory="""Você é um desenvolvedor especialista com profundo conhecimento nas tecnologias 
        solicitadas. Sua função é garantir que as tecnologias sejam aplicadas de forma adequada, 
        seguindo boas práticas e padrões modernos de desenvolvimento.""",
        verbose=True,
        llm=llm,
    )
    
    task_designer = Agent(
        role="Designer de Tarefas",
        goal="Criar um conjunto de tarefas claras e progressivas para o desenvolvimento do projeto",
        backstory="""Você é especializado em quebrar projetos complexos em tarefas menores e gerenciáveis. 
        Sua função é criar uma sequência de tarefas que guie o desenvolvedor do básico até a 
        conclusão do projeto completo.""",
        verbose=True,
        llm=llm,
    )
    
    # Descrição das tecnologias
    tech_str = ", ".join(technologies)
    
    # Tarefas
    project_definition = Task(
        description=f"""
        Crie uma proposta de projeto {project_type} utilizando as seguintes tecnologias: {tech_str}.
        {f'Informações adicionais: {additional_info}' if additional_info else ''}
        
        O projeto deve ser:
        1. Desafiador mas realizável
        2. Aplicável ao mundo real
        3. Focado nas tecnologias solicitadas
        
        Entregue:
        - Um título atraente para o projeto
        - Uma descrição detalhada
        - 3-5 objetivos principais
        """,
        agent=project_manager,
    )
    
    technology_analysis = Task(
        description=f"""
        Analise as tecnologias solicitadas ({tech_str}) e estruture como elas serão utilizadas no projeto.
        
        Considere:
        1. Como as tecnologias se relacionam entre si
        2. Quais são as funcionalidades chave que poderão ser implementadas
        3. Arquitetura geral do sistema
        
        Entregue:
        - Uma lista final das tecnologias principais e complementares necessárias
        - Recomendações técnicas para a implementação
        """,
        agent=tech_specialist,
    )
    
    task_creation = Task(
        description=f"""
        Com base na definição do projeto e na análise tecnológica, crie uma sequência de 5-8 tarefas 
        de desenvolvimento para guiar o usuário a construir este projeto.
        
        Cada tarefa deve:
        1. Ter um título claro
        2. Incluir uma descrição detalhada do que deve ser feito
        3. Ser sequencial e progressiva
        
        As tarefas devem começar do básico (configuração, estrutura) e evoluir até os 
        recursos mais complexos do projeto.
        """,
        agent=task_designer,
        dependencies=[project_definition, technology_analysis]
    )
    
    # Criação da crew e execução
    crew = Crew(
        agents=[project_manager, tech_specialist, task_designer],
        tasks=[project_definition, technology_analysis, task_creation],
        verbose=2,
        process=Process.sequential,
    )
    
    result = crew.kickoff()
    
    # Processamento dos resultados
    try:
        # Extraindo informações dos resultados
        final_result = parse_crew_results(result, technologies)
        return final_result
    except Exception as e:
        print(f"Erro ao processar resultados: {e}")
        # Fallback para resultado padrão em caso de erro
        return {
            "title": f"Projeto {project_type.capitalize()} com {technologies[0]}",
            "description": f"Desenvolva um projeto {project_type} utilizando {tech_str}.",
            "goals": ["Criar um projeto funcional", "Aplicar as tecnologias solicitadas", "Seguir boas práticas"],
            "tasks": [
                {"title": "Configuração inicial", "description": "Configure o ambiente de desenvolvimento"},
                {"title": "Estrutura básica", "description": "Implemente a estrutura básica do projeto"},
                {"title": "Implementação das funcionalidades", "description": "Desenvolva as funcionalidades principais"},
                {"title": "Testes e validação", "description": "Teste e valide o funcionamento do projeto"},
                {"title": "Finalização", "description": "Finalize o projeto e prepare para entrega"}
            ],
            "technologies": technologies
        }

def parse_crew_results(raw_result: str, technologies: List[str]) -> Dict[str, Any]:
    """
    Processa os resultados da Crew e formata como proposta de projeto.
    
    Na prática, seria necessário um parser mais robusto, mas este é um exemplo simplificado.
    """
    try:
        # Em um cenário real, usaríamos regex ou LLM para extrair informações estruturadas
        # do texto de resposta da Crew. Esta é uma implementação simplificada.
        
        lines = raw_result.strip().split('\n')
        
        title = "Novo Projeto"
        description = ""
        goals = []
        tasks = []
        
        # Encontrar título
        for line in lines:
            if line.strip() and not line.startswith('-') and not line.startswith('#') and len(line.strip()) < 100:
                title = line.strip()
                break
        
        # Extrair descrição (simplificado)
        description_start = False
        description_lines = []
        for line in lines:
            if "descrição" in line.lower() or "description" in line.lower():
                description_start = True
                continue
            if description_start and line.strip() and not "objetivo" in line.lower() and not "goal" in line.lower():
                if line.startswith('-') or line.startswith('#'):
                    description_start = False
                else:
                    description_lines.append(line.strip())
            elif description_start and ("objetivo" in line.lower() or "goal" in line.lower()):
                description_start = False
        
        description = " ".join(description_lines)
        
        # Extrair objetivos
        in_goals = False
        for line in lines:
            if "objetivo" in line.lower() or "goal" in line.lower() or "meta" in line.lower():
                in_goals = True
                continue
            if in_goals and line.strip().startswith('-'):
                goals.append(line.strip()[2:].strip())
            elif in_goals and line.strip().startswith('1.'):
                in_goals = False
            
        # Extrair tarefas
        in_tasks = False
        current_task = None
        
        for line in lines:
            if "tarefa" in line.lower() or "task" in line.lower():
                in_tasks = True
                continue
            
            if in_tasks and line.strip():
                if line.strip().startswith('-') or line.strip().startswith('Task') or any(str(i) in line[:5] for i in range(1, 10)):
                    if current_task:
                        tasks.append(current_task)
                    
                    parts = line.strip().split(':', 1)
                    if len(parts) > 1:
                        title = parts[0].strip('-: 0123456789TasktaskTarefa')
                        desc = parts[1].strip()
                    else:
                        title = line.strip('-: 0123456789TasktaskTarefa')
                        desc = ""
                    
                    current_task = {"title": title, "description": desc}
                elif current_task:
                    current_task["description"] += " " + line.strip()
        
        # Adicionar a última tarefa se existir
        if current_task:
            tasks.append(current_task)
        
        # Garantir que temos pelo menos algumas tarefas
        if len(tasks) < 3:
            tasks = [
                {"title": "Configuração do projeto", "description": "Configurar ambiente de desenvolvimento e estrutura inicial."},
                {"title": "Implementação básica", "description": "Implementar as funcionalidades básicas do projeto."},
                {"title": "Funcionalidades avançadas", "description": "Adicionar recursos avançados e refinar o projeto."},
                {"title": "Testes e documentação", "description": "Adicionar testes e documentar o projeto."},
                {"title": "Finalização", "description": "Revisar o código, corrigir bugs e preparar para entrega."}
            ]
        
        # Garantir que temos objetivos
        if len(goals) < 2:
            goals = [
                "Desenvolver um projeto completo e funcional",
                "Implementar todas as tecnologias solicitadas de forma coerente",
                "Seguir boas práticas de desenvolvimento"
            ]
        
        return {
            "title": title,
            "description": description if description else f"Projeto utilizando {', '.join(technologies)}",
            "goals": goals[:5],  # Limitando a 5 objetivos
            "tasks": tasks[:8],  # Limitando a 8 tarefas
            "technologies": technologies
        }
        
    except Exception as e:
        print(f"Erro ao analisar resultados: {e}")
        # Retornar uma resposta padrão em caso de erro
        return {
            "title": f"Projeto com {', '.join(technologies[:2])}",
            "description": f"Desenvolva um projeto utilizando {', '.join(technologies)}.",
            "goals": ["Criar um projeto funcional", "Implementar as tecnologias solicitadas"],
            "tasks": [
                {"title": "Configuração inicial", "description": "Configure o ambiente de desenvolvimento"},
                {"title": "Desenvolvimento principal", "description": "Implemente as funcionalidades principais"},
                {"title": "Finalização", "description": "Finalize o projeto e prepare para entrega"}
            ],
            "technologies": technologies
        } 