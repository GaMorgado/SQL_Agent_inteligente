from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import load_prompt
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from handler.config import ExecutionState
from typing import Dict
import os

@tool
def query_generate(question: str) -> str: 
    """
    This tool is useful for generating an SQL query to retrieve information
    about customers, products, or transactions based on a user question.
    Input: a string containing the user's question.
    Output: a string containing only the generated SQL query.
    """
    print(f"Pergunta recebida pela ferramenta: {question}")

    #carregando prompt da ferramenta
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        query_tool_prompt_path = os.path.join(parent_dir, "prompts", "query_tool_prompt.json")
    except Exception as e:
        return 'ERRO_FERRAMENTA: não foi construir o caminho para o prompt'
        
    #formatando o prompt com a pergunta do usuario
    try:
        query_tool_prompt = load_prompt(query_tool_prompt_path, encoding="utf-8")
        formatted_prompt = query_tool_prompt.format(user_question=question)
    except Exception as e: 
        return 'ERRO_FERRAMENTA: Não foi possível carregar o prompt para geração da query baseada na pergunta do usuário'

    print(f"Prompt formatado para o LLM da ferramenta:\n{formatted_prompt}")

    #gerando query para pesquisa no banco
    try:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        messages = [HumanMessage(content=formatted_prompt)]
        ai_message_output = llm.invoke(messages)
        #setando a query gerada apartir da pergunta do usuario
        sql_query = ""
        if isinstance(ai_message_output, AIMessage) and hasattr(ai_message_output, 'content'):
            sql_query = ai_message_output.content
        elif isinstance(ai_message_output, str):
            sql_query = ai_message_output
    except Exception as e: 
        return 'ERRO_FERRAMENTA: Não foi possível gerar a query'
    
    #limpando a query
    if sql_query.strip().lower().startswith("```sql"):
        sql_query = sql_query.strip()[5:]
        if sql_query.strip().endswith("```"):
            sql_query = sql_query.strip()[:-3]
    elif sql_query.strip().startswith("```"):
        sql_query = sql_query.strip()[3:]
        if sql_query.strip().endswith("```"):
            sql_query = sql_query.strip()[:-3]

    #devolvendo a query
    return sql_query.strip()

def SQLGenerateAgent(state: ExecutionState) -> Dict[str, str]:
    """Nó do langgraph referente ao agent de criação de consultas SQL"""

    user_input = state.user_question

    if not user_input:
        return {"error": "Pergunta do utilizador não fornecida para o agente SQL."}

    agent_sql_prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente de IA especializado em gerar consultas SQL...\n" 
                "O banco possui as seguintes tabelas:\n\n"
                "Tabela 'clientes':\n"
                "- id_cliente INT PRIMARY KEY NOT NULL\n"
                "Após gerar a SQL, devolva apenas a consulta SQL na chave 'output'.\n"
                "Se a pergunta não for possível de ser respondida com base nesse esquema, retorne:\n"
                "'Erro: pergunta não compreendida ou inválida para o banco de dados.'"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    toolkit = [query_generate]
    llm_agent_sql = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    generated_sql = ""
    try:
        agent = create_openai_tools_agent(llm=llm_agent_sql, tools=toolkit, prompt=agent_sql_prompt)
        agent_executor = AgentExecutor(agent=agent, tools=toolkit, verbose=True, handle_parsing_errors=True)
        query = agent_executor.invoke({"input": user_input})       
        if isinstance(query, dict) and "output" in query:
            generated_sql = query['output']
    except Exception as e:
        return {'error': f'Erro ao executar agente de criação de queries SQL, erro: {e}'}

    print(f"Query gerada pelo agente SQL: {generated_sql}")

    return {"generated_query": generated_sql}
