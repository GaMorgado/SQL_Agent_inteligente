from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver
import os
import traceback
from handler.config import ExecutionState 
from handler.db_connection import engine   
from dotenv import load_dotenv

load_dotenv()

checkpointer_db_url = os.getenv("CHECKPOINTER_DATABASE_URL")
print(checkpointer_db_url)

# Verificação crítica se a engine foi carregada corretamente
if engine is None:
    print("ERRO FATAL: A engine do banco de dados não foi inicializada. O programa será encerrado.")
    exit()

# Criação do grafo e orquestração
workflow = StateGraph(ExecutionState)

# Importação e adição dos nós dos agents
try:
    from agents.InputParseNplAgent import InputParseAgent
    from agents.SQLAgent import SQLGenerateAgent
    from agents.ValidatorAgent import ValidatorAgent
    from agents.QueryExecutorAgent import QueryExecutorAgent
    from agents.ResponseAgent import ResponseAgent
    from handler.error_handler import error_handler

    workflow.add_node("user_input_parser", InputParseAgent)
    workflow.add_node("sql_generate_agent", SQLGenerateAgent)
    workflow.add_node("query_validator_agent", ValidatorAgent)
    workflow.add_node("query_executor_agent", QueryExecutorAgent)
    workflow.add_node("response_formatting_agent", ResponseAgent)
    workflow.add_node("error_handler", error_handler)

except ImportError as e:
    print(f"ERRO CRÍTICO: Falha ao importar um ou mais agents/handlers: {e}")
    print("Verifique se os arquivos e classes/funções dos agents estão corretos.")
    traceback.print_exc()
    exit()
except Exception as e_setup: 
    print(f"ERRO CRÍTICO durante a configuração dos nós do workflow: {e_setup}")
    traceback.print_exc()
    exit()


# Funções de roteamento (permanecem as mesmas)
def verify_error_input_parse(state: ExecutionState) -> str:
    if state.error:
        return "error_handler"
    return "sql_generate_agent"

def verify_error_sql_generate(state: ExecutionState) -> str:
    if state.error or not state.generated_query:
        return "error_handler"
    return "query_validator_agent"

def verify_error_sql_validate(state: ExecutionState) -> str:
    if state.error or not state.validated_query:
        return "error_handler"
    return "query_executor_agent"

def verify_error_query_execution(state: ExecutionState) -> str:
    if state.error:
        return "error_handler"
    if isinstance(state.db_result, dict) and state.db_result.get("status") == "error":
        return "error_handler"
    return "response_formatting_agent"

def verify_error_response_formatting(state: ExecutionState) -> str:
    if state.error:
        return "error_handler"
    return END

# Configuração dos edges (permanece a mesma)
workflow.set_entry_point("user_input_parser")
workflow.add_conditional_edges("user_input_parser", verify_error_input_parse, {"error_handler": "error_handler", "sql_generate_agent": "sql_generate_agent"})
workflow.add_conditional_edges("sql_generate_agent", verify_error_sql_generate, {"error_handler": "error_handler", "query_validator_agent": "query_validator_agent"})
workflow.add_conditional_edges("query_validator_agent", verify_error_sql_validate, {"error_handler": "error_handler", "query_executor_agent": "query_executor_agent"})
workflow.add_conditional_edges("query_executor_agent", verify_error_query_execution, {"error_handler": "error_handler", "response_formatting_agent": "response_formatting_agent"})
workflow.add_conditional_edges("response_formatting_agent", verify_error_response_formatting, {"error_handler": "error_handler", END: END})
workflow.add_edge("error_handler", END)

# Função executar_fluxo_do_agente (permanece a mesma)
def executar_fluxo_do_agente(compiled_app, thread_id_input_func=input):
    print("Iniciando o fluxo do Agente SQL Inteligente...")

    estado_inicial_input = {}
    try:
        thread_id = thread_id_input_func("Insira o seu nome (ou ID da thread) para futuras consultas: ")
        if not thread_id:
            print("ID da thread não pode ser vazio. Abortando.")
            return
        config = {"configurable": {"thread_id": thread_id}}
        resultado_final_do_estado = compiled_app.invoke(estado_inicial_input, config=config)
        print("\n--- FLUXO CONCLUÍDO --- ")
        print(resultado_final_do_estado)
        print(f"pergunta do usuario: -{resultado_final_do_estado['user_question']}")
        print(f"resposta do assistente: -{resultado_final_do_estado['formatted_answer']}\n")

        if len(resultado_final_do_estado['chat_history']) > 0:
            print("histórico de chat:")
            for n in resultado_final_do_estado['chat_history']:
                print(f"{n}")

    except Exception as e:
        print(f"\n Ocorreu uma exceção não tratada ao executar o grafo principal: {e}")
        traceback.print_exc()

# Bloco principal de execução (permanece o mesmo, incluindo a advertência sobre checkpointer.setup())
if __name__ == "__main__":
    if not checkpointer_db_url:
        print("ERRO CRÍTICO: CHECKPOINTER_DATABASE_URL não está definida. Não é possível iniciar o checkpointing.")
    else:
        with PostgresSaver.from_conn_string(checkpointer_db_url) as checkpointer:
            try:
                checkpointer.setup()
            except AttributeError:
                print("checkpointer.setup() não é um método válido para este objeto checkpointer e foi ignorado.")
            except Exception as e_setup:
                print(f"ERRO ao chamar checkpointer.setup(): {e_setup}")
            
            app = workflow.compile(checkpointer=checkpointer)

            
            executar_fluxo_do_agente(app, input)