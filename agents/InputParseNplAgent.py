from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain.prompts import load_prompt
from typing import Dict
from handler.config import ExecutionState
import os

def InputParseAgent(state: ExecutionState) -> Dict[str, str]:
    """Nó que recolhe a pergunta do utilizador e a reformula usando um LLM."""
    user_input = input("Bem vindo ao sistema de verificação de transações, faça sua pergunta: ")

    novo_historico = state.chat_history + [f"Utilizador: {user_input.strip()}"]

    #constroi o caminho do prompt 
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        input_prompt_path = os.path.join(parent_dir, "prompts", "InputParseNpl_agent_prompt.json")
    except Exception as e:
        return {'error': f'Erro ao construir o caminho do prompt {e}'}   

    #carrega o caminho do prompt
    try:
        input_prompt = load_prompt(input_prompt_path, encoding="utf-8")
        formatted_input_parse_prompt = input_prompt.format(user_input=user_input)
    except Exception as e:
        return {'error': f'Não foi possível carregar o prompt para melhorar a pergunta do usuario, erro: {e}'}

    #invoca a LLM para gerar a resposta
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        messages = [HumanMessage(content=formatted_input_parse_prompt)]
        ai_message_response = llm.invoke(messages)
        formatted_question = ''
        if isinstance(ai_message_response, AIMessage) and hasattr(ai_message_response, 'content'):
            formatted_question = ai_message_response.content
        elif isinstance(ai_message_response, str):
            formatted_question = ai_message_response
    except Exception as e:
        return {'error': f'Não foi possível gerar a pergunta melhorada do usuario, erro: {e}'}

    print(f"Pergunta original: {user_input}")
    print(f"Pergunta reformulada: {formatted_question.strip()}")

    return {'user_question': formatted_question.strip(), 'chat_history': novo_historico}