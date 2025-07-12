from fastapi import APIRouter
from app.schemas.interview import QuestionRequest, ResponseRequest
from app.services.openai_service import generate_ai_reply, generate_completion
import random

router = APIRouter()

# Static mock questions dictionary
mockQuestions = {
    # Paste your large mockQuestions object here from the original file
}

@router.post("/question")
def generate_question(payload: QuestionRequest):
    topic = payload.type
    difficulty = payload.difficulty
    isFirst = payload.isFirst

    questions = mockQuestions.get(topic, {}).get(difficulty, [])
    if not questions:
        fallback = f"Let's start with a {difficulty.lower()} {topic} question: Can you tell me about your experience with {topic}?"
        return {"question": fallback}

    random_question = random.choice(questions)
    if isFirst:
        question = f"Hello! I'm your AI interviewer today. We'll be conducting a {topic} interview at {difficulty} level. Let's start with this question: {random_question}"
    else:
        question = random_question

    return {"question": question}


@router.post("/response")
def generate_response(payload: ResponseRequest):
    type = payload.type
    difficulty = payload.difficulty
    user_response = payload.userResponse
    history = payload.conversationHistory
    count = payload.questionCount

    should_ask_new = count < 5 and random.random() > 0.3

    system_prompt = f"""You are an expert {type} interviewer conducting a {difficulty.lower()} level interview.
    
The candidate just responded: "{user_response}"

Your task:
1. Briefly acknowledge their response (1-2 sentences)
2. {"Ask a new question" if should_ask_new else "Ask a follow-up question to dive deeper"}

Keep it professional, conversational, and do not give full feedback now.
"""

    context = "\n".join([f'{msg["role"]}: {msg["content"]}' for msg in history[-4:]])

    prompt = f"Conversation context:\n{context}\n\nCandidate's latest response: {user_response}"

    try:
        ai_text = generate_completion(prompt=prompt, system_prompt=system_prompt)
        return {"response": ai_text, "isNewQuestion": should_ask_new}
    except Exception as e:
        return {"error": "Failed to generate response", "details": str(e)}
