import tiktoken
from typing import List

def token_controller_for_chat_history(list_msg: List[str] ) -> List[str]:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens_per_message = [len(encoding.encode(msg)) for msg in list_msg]
    total_tokens = sum(tokens_per_message)

    while total_tokens > 1024:

        total_tokens -= tokens_per_message.pop(0)

        list_msg.pop(0)
    
        if not list_msg:
            break
        
    print(f"Total de tokens final: {total_tokens}")
    return list_msg