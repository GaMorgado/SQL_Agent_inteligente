from handler.config import ExecutionState
from handler.db_connection import engine
from sqlalchemy import text, exc
from typing import Any, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, tool, AgentExecutor

@tool
def databaseAccess(query: str) -> Dict[str, Any]:
    """
        Executes an SQL query in the PostgreSQL database and returns the result.
        Use this tool when you have a validated SQL query ready to be executed.
        Input: query_sql (str) - The SQL query to be executed.
        Output: A dictionary with 'data' (a list of dictionaries for SELECT queries, or the number of affected rows for DML)
        or 'error' if an issue occurs.
    """
    if engine is None:
        return {"status": "error", "query_type": "configuration_error", "data": None, "message": "Erro crítico: A engine do banco de dados não está configurada."}
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            if result.returns_rows:
                column_names = list(result.keys())
                data = [dict(zip(column_names, row)) for row in result.fetchall()]
                print(f"INFO: Resultado do SELECT: {len(data)} linhas.")
                connection.commit()
                return {"status": "success", "query_type": "select" ,"data": data, "message": f"{len(data)} linhas retornadas"}
            else:
                row_count = result.rowcount
                connection.commit()
                print(f"INFO: Comando DML executado. Linhas afetadas: {row_count}")
                return {"status": "success", "query_type": "dml", "rows_affected": row_count, "message": f"Comando executado com sucesso, {row_count} linhas afetadas."}
    except exc.SQLAlchemyError as e:
        print(f"ERRO: Erro de banco de dados ao executar query: {query}. Erro: {str(e)}")
        return {"status": "error", "query_type": "database_error", "data": None, "message": f"Erro de banco de dados: {str(e)}"}
    except Exception as e:
        print(f"ERRO: Erro inesperado na ferramenta databaseAccess com query: {query}. Erro: {str(e)}")
        return {"status": "error", "query_type": "tool_error", "data": None, "message": f"Erro inesperado na ferramenta: {str(e)}"}

def QueryExecutorAgent(state: ExecutionState) -> dict:
    """Nó que utiliza a query gerada para efetuar a consulta no banco"""

    validated_query = state.validated_query
    current_chat_history = state.chat_history if state.chat_history is not None else []

    if not validated_query:
        return {'error': 'Não foi enviada a query para a execução', 'chat_history': current_chat_history}

    print(f"INFO: Query validada para execução: {validated_query}")

    # prompt do agente executor
    executor_agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "Você é um agente executor de SQL altamente eficiente e preciso.\n"
                "Sua única tarefa é executar a query SQL fornecida usando a ferramenta 'acessaBanco'.\n"
                "NÃO modifique a query de forma alguma.\n"
                "Apenas execute a query exatamente como ela é fornecida através da ferramenta.\n"
                "Retorne o resultado da execução da ferramenta diretamente."
            ),
        ),
        (
            "human",
            "Por favor, execute a seguinte query SQL: {validated_query}"
        ),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    toolkit = [databaseAccess]

    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        langchain_executor_agent = create_openai_tools_agent(llm=llm, tools=toolkit, prompt=executor_agent_prompt)
        agent_runner = AgentExecutor(agent=langchain_executor_agent, tools=toolkit, verbose=True, handle_parsing_errors=True)
        
        agent_input = {"validated_query": validated_query}

        agent_response = agent_runner.invoke(agent_input)

        # A resposta do AgentExecutor geralmente está na chave 'output'
        if isinstance(agent_response, dict) and "output" in agent_response:
            execution_result = agent_response["output"]
        else:
            print(f"AVISO: Estrutura de resposta inesperada do agente: {agent_response}. Usando a resposta completa.")
            execution_result = agent_response


    except Exception as e:
        print(f"ERRO: Exceção ao executar o QueryExecutorAgent: {e}")
        import traceback
        traceback.print_exc()
        return {'error': f'Erro ao executar query com o agente: {str(e)}', 'chat_history': current_chat_history}

    return {"db_result": execution_result}