import requests
import openai 
from app.core.config import OPENAI_API_KEY, CHAT_COMPLETION_URL
import json

openai.api_key = OPENAI_API_KEY


def generate_completion(prompt: str, system_prompt: str, model: str = "gpt-4.1-nano") -> str:
    url = CHAT_COMPLETION_URL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "model": model,
        "max_tokens": 1000,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        # Adjust the following line based on the actual API response structure
        return data["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
    



def generate_ai_reply(prompt: str, system_prompt: str, model: str = "gpt-4o") -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]
    




def generate_interview_feedback(conversation, topic, difficulty, model="gpt-4o") -> str:
    messages = [
        {"role": "system", "content": f"You are an expert interviewer in {topic} at {difficulty} level. Evaluate the following mock interview."},
        {"role": "user", "content": "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation])},
    ]

    response = openai.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content.strip()


def generate_completion_feedback(conversation, topic, difficulty, model: str = "gpt-4.1-nano") -> str:
    
    system_prompt = f"""
You are a senior technical interviewer. Evaluate the following {topic} mock interview (difficulty: {difficulty}).
Provide a structured JSON feedback with the following fields:

1. score (0–100) - integer
2. strengths - list of 3 bullet points
3. improvements - list of 3 bullet points
4. suggestions - list of 3 personalized improvement tips
5. detailedAnalysis - 1 paragraph detailed feedback

Respond with only valid JSON. No explanations.
"""

    url = CHAT_COMPLETION_URL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation])}
    ]
    payload = {
        "messages": messages,
        "model": model,
        "max_tokens": 1000,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
            data = response.json()
            try:
                content = data["choices"][0]["message"]["content"]
                return json.loads(content)  # convert OpenAI JSON string to dict
            except Exception as e:
                raise Exception(f"Failed to parse OpenAI feedback JSON: {e}")
    else:
        raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")