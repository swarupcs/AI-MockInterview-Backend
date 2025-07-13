import requests
import openai 
from app.core.config import OPENAI_API_KEY, CHAT_COMPLETION_URL

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
    
    
