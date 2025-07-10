import os
from openai import OpenAI
from dotenv import load_dotenv

class Categorize:
    def __init__(self):
        self.dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.env')
        load_dotenv(self.dotenv_path)

    def OpenAi(self, message):
        result = []
        api_key = os.getenv('OPENAI_API_KEY')

        if not api_key:
            result.append('unknown')
            result.append('OpenAI API key not found!')
            client = OpenAI(api_key=api_key)
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": (
                        "Определи категорию жалобы. Варианты: техническая, оплата, другое. "
                        "Ответ только одним словом. - " + message
                    )
                }]
            )
            result.append(response.choices[0].message.content.strip())
        except Exception as e:
            result.append('unknown')
            result.append(f"OpenAI API error: {e}")
        return result

CATEGORIZE = Categorize()