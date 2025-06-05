from handler.config import ExecutionState
from typing import Dict, Any

def error_handler(state:ExecutionState) -> Dict[str, Any]:
    """Nó que lida com os erros e expões para o usuário"""
    error_message_from_state = state.error

    current_chat_history = []
    if hasattr(state, 'chat_history') and state.chat_history is not None:
        current_chat_history = state.chat_history.copy()

    user_message_error = ""
    if not error_message_from_state:
        user_message_error = "Ocorreu um problema inesperado, mas não foi possível identificar o erro específico."
        return {"formatted_answer": user_message_error,"chat_history": current_chat_history,"error": "Tratador de erros invocado sem erro explícito no estado."}

    user_message_error = f"Desculpe, ocorreu um problema ao processar o seu pedido. Detalhes: {error_message_from_state.strip()}"
    current_chat_history.append(f"Agente (Erro): {user_message_error}")

    return {"formatted_answer": user_message_error, "chat_history": current_chat_history,"error": error_message_from_state}
