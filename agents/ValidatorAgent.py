from langchain.prompts import load_prompt
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from handler.config import ExecutionState
from typing import Dict
import os

def ValidatorAgent(state: ExecutionState) -> Dict[str, str]:
    """Nó que valida a query  gerada e manda uma query validada"""

    invalidated_query = state.generated_query

    if not invalidated_query:
        return {"error": "Nenhuma query fornecida para validação."}

    print(f"Query recebida para validação: {invalidated_query}")

    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        validator_prompt_path = os.path.join(parent_dir, "prompts", "ValidatorQuery_agent_prompt.json")
    except Exception as e:
        return {'error': f'Erro ao construir o caminho do prompt, erro: {e}'} 

    try: 
        validator_prompt = load_prompt(validator_prompt_path, encoding="utf-8")
        formatted_validator_prompt = validator_prompt.format(generated_query=invalidated_query)
    except Exception as e:
        return {'error': f'Erro ao carregar o prompt, erro: {e}'} 
    
    print(f"Prompt formatado para LLM (Validator): {formatted_validator_prompt}")

    validated_query = ""
    try: 
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        messages = [HumanMessage(content=formatted_validator_prompt)]
        ai_message_response = llm.invoke(messages)

        if isinstance(ai_message_response, AIMessage) and hasattr(ai_message_response, 'content'):
            validated_query = ai_message_response.content
        elif isinstance(ai_message_response, str):
            validated_query = ai_message_response
    except Exception as e:
        return {'error': f'Erro ao validar query com o agent, erro: {e}'} 

    if validated_query.strip().lower().startswith("```sql"):
        validated_query = validated_query.strip()[5:]
        if validated_query.strip().endswith("```"):
            validated_query = validated_query.strip()[:-3]
    elif validated_query.strip().startswith("```"):
        validated_query = validated_query.strip()[3:]
        if validated_query.strip().endswith("```"):
            validated_query = validated_query.strip()[:-3]

    print(f"Query após tentativa de validação/correção: {validated_query.strip()}")
    
    return {"validated_query": validated_query.strip()}