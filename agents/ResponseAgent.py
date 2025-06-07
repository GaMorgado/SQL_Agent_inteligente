from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain.prompts import load_prompt
from handler.config import ExecutionState
from handler.token_counter import token_controller_for_chat_history
from typing import Dict
import os
import json

def ResponseAgent(state:ExecutionState) -> Dict[str, str]:
    """Nó que utiliza o resultado da query para devolver uma resposta para o usuario"""

    result_query_obj = state.db_result

    chat_history = state.chat_history

    controlled_chat_history = token_controller_for_chat_history(chat_history)

    chat_history_str = "\n".join(controlled_chat_history)

    if not result_query_obj:
        return {'error': "Não houve resultados para apresentar."}
    
    if isinstance(result_query_obj, dict):
        query_result_str = json.dumps(result_query_obj, ensure_ascii=False, indent=2)
    else:
        query_result_str = str(result_query_obj)

    print(f"resultado do banco em str: {result_query_obj}")

    try: 
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        ResponseAgent_prompt_path = os.path.join(parent_dir, "prompts", "Response_agent_prompt.json")
    except Exception as e:
        return {'error': f'Erro ao construir o caminho do prompt, erro: {e}'}

    try: 
        response_prompt = load_prompt(ResponseAgent_prompt_path, encoding="utf-8")
        formatted_responde_prompt = response_prompt.format(query_result=query_result_str, chat_history=chat_history_str)
    except: 
        return {'error': f'Erro ao carregar o prompt, erro: {e}'}  

    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9)
        messages = [HumanMessage(content=formatted_responde_prompt)]
        ai_message_response = llm.invoke(messages)

        formatted_response = ''
        if isinstance(ai_message_response, AIMessage) and hasattr(ai_message_response, 'content'):
            formatted_response = ai_message_response.content
        elif isinstance(ai_message_response, str):
            formatted_response = ai_message_response
    except Exception as e: 
        return {'error': f'Erro ao gerar resposta com o resultado da query para o usuario, erro: {e}'} 
    
    print(f"resposta final: {formatted_response}")

    novo_historico = state.chat_history + [f"Agente: {formatted_response.strip()}"]
    return {'formatted_answer': formatted_response.strip(), 'chat_history': novo_historico}