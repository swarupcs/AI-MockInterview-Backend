from fastapi import APIRouter
from app.schemas.interview import QuestionRequest, ResponseRequest, FeedbackRequest, FeedbackResponse
from app.services.openai_service import generate_ai_reply, generate_completion, generate_interview_feedback, generate_completion_feedback
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
    is_first = payload.isFirst

    questions = mockQuestions.get(topic, {}).get(difficulty, [])
    if not questions:
        fallback = f"Let's begin with a {difficulty.lower()} {topic} question: Can you tell me about your experience with {topic}?"
        return {"question": fallback}

    if is_first:
        if topic == "Frontend":
            question = (
                f"Welcome! As your AI interviewer, we're conducting a {difficulty} Frontend interview.\n"
                f"To begin, can you share your strongest area in Frontend (e.g., HTML, CSS, JavaScript, React)?"
            )
        elif topic == "Backend":
            question = (
                f"Hi there! Let's start your {difficulty} Backend interview.\n"
                f"What technologies or concepts do you feel most confident with — APIs, databases, authentication, or others?"
            )
        else:
            question = (
                f"Hello! I'm your AI interviewer today. We'll be conducting a {topic} interview at {difficulty} level. "
                f"Let's begin with this question: {random.choice(questions)}"
            )
    else:
        question = random.choice(questions)

    return {"question": question}


@router.post("/response")
def generate_response(payload: ResponseRequest):
    topic = payload.type
    difficulty = payload.difficulty
    user_response = payload.userResponse
    history = payload.conversationHistory
    count = payload.questionCount

    should_ask_new = count < 5 and random.random() > 0.3

    # Context from the last 4 messages
    context = "\n".join([f'{msg["role"]}: {msg["content"]}' for msg in history[-4:]])

    # Tailored system prompt
    if topic == "Frontend":
        system_prompt = f"""
You are a seasoned Frontend interviewer conducting a {difficulty.lower()} level interview.

The candidate has just said: "{user_response}"

1. Briefly acknowledge the response.
2. If they mentioned React, JavaScript, HTML, or CSS — ask deeper or practical questions in that area.
3. Otherwise, move progressively from HTML/CSS → JS → React → performance/security.

Keep tone friendly but professional. No feedback yet. Just ask meaningful, increasingly insightful questions.
"""
    elif topic == "Backend":
        system_prompt = f"""
You're an expert Backend interviewer running a {difficulty.lower()} interview.

Given the candidate's answer: "{user_response}",

- Ask deeper questions based on their answer.
- Touch on topics like REST APIs, databases, authentication, scaling, or error handling.

Remain professional and focused. No evaluation yet.
"""
    else:
        system_prompt = f"""
You are an expert {topic} interviewer conducting a {difficulty.lower()} level interview.

The candidate responded: "{user_response}"

1. Acknowledge the response briefly.
2. { "Ask a new question" if should_ask_new else "Ask a deeper follow-up question" }

Avoid full feedback. Keep it conversational and focused.
"""

    prompt = f"Recent conversation:\n{context}\n\nCandidate's response: {user_response}"

    try:
        ai_text = generate_completion(prompt=prompt, system_prompt=system_prompt)
        return {"response": ai_text, "isNewQuestion": should_ask_new}
    except Exception as e:
        return {"error": "Failed to generate response", "details": str(e)}




@router.post("/feedback", response_model=FeedbackResponse)
def get_feedback(request: FeedbackRequest):
    feedback = generate_completion_feedback(
        conversation=[msg.dict() for msg in request.conversationHistory],
        topic=request.type,
        difficulty=request.difficulty
    )
    return feedback 