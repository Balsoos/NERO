# app/services/openai_service.py

import openai
import json
from app.config import Config

# Initialize OpenAI API key
openai.api_key = Config.OPENAI_API_KEY

def parse_task_input(natural_language_input: str):
    """
    Use OpenAI to parse the natural language input and extract task details.
    """
    prompt = f"""
    Extract the following information from the user's input:
    - Task description
    - Due date and time (ISO 8601 format)
    - Priority level (low, medium, high)

    Format the output as JSON with keys: 'description', 'due_date', 'priority'.
    If any information is missing, set its value to null.

    User Input: "{natural_language_input}"
    """

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or 'gpt-3.5-turbo' if using chat models
            prompt=prompt,
            max_tokens=150,
            temperature=0,
        )
        extracted_text = response.choices[0].text.strip()
        # Ensure the response is valid JSON
        task_data = json.loads(extracted_text)
        return task_data
    except Exception as e:
        print(f"Error in OpenAI API: {e}")
        return None
