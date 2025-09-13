# core/llm_connector.py
import os
from openai import OpenAI

# Load API key (set as environment variable for safety)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_llm(prompt: str, system_role: str = "You are ANNA, an ethical scientific advisor.") -> str:
    """
    Send a query to the LLM (OpenAI GPT) and return its response.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # fast, strong reasoning
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,  # low randomness for science
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM Error: {str(e)}"
