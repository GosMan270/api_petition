import os
from openai import OpenAI
from dotenv import load_dotenv

class Categorize:
    def __init__(self):
        self.dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.env')
        load_dotenv(self.dotenv_path)

    def OpenAi(self, message):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("OpenAI API key not found!")
            return "unknown"
        client = OpenAI(api_key=api_key)
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Твоя задача только определить к какой категории относиться следующая жалоба! - {message}. ДАЙ ОТВЕТ ТОЛЬКО 1 СЛОВОМ"}]
            )
            result = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API error: {e}")
            result = "unknown"
        return result

CATEGORIZE = Categorize()