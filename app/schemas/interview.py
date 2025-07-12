from pydantic import BaseModel
from typing import List, Literal

QuestionTypes = Literal["DSA", "Behavioral", "System Design", "Frontend", "Backend", "Product Management"]
DifficultyLevels = Literal["Easy", "Medium", "Hard"]

class QuestionRequest(BaseModel):
    type: QuestionTypes
    difficulty: DifficultyLevels
    isFirst: bool

class ResponseRequest(BaseModel):
    type: QuestionTypes
    difficulty: DifficultyLevels
    userResponse: str
    conversationHistory: List[dict]  # [{role: "user"|"assistant", content: "..."}, ...]
    questionCount: int
