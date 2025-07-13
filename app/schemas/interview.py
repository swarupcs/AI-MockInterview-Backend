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
# Each message in conversation history
class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

# Feedback request schema
class FeedbackRequest(BaseModel):
    type: QuestionTypes
    difficulty: DifficultyLevels
    conversationHistory: List[ChatMessage]

# Feedback response schema
class FeedbackResponse(BaseModel):
    feedback: str