from typing import Optional, List, Any
from pydantic import BaseModel, Field

class ExecutionState(BaseModel):
    user_question: Optional[str] = None
    generated_query: Optional[str] = None
    validated_query: Optional[str] = None
    db_result: Optional[Any] = None
    formatted_answer: Optional[str] = None
    error: Optional[str] = None
    chat_history: List[str] = Field(default_factory=list)