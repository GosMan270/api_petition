import os
import aiohttp
import asyncio
from openai import OpenAI
from dotenv import load_dotenv



class Categorize:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config.env')
        load_dotenv(dotenv_path)

    async def OpenAi(self, message):
        api_key = os.getenv('OPENAI_API_KEY')
        test_mode = bool(os.getenv('Test_Mode'))
        print(test_mode)
        url = 'http://fastapi_test:7000/category'

        if test_mode:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    try:
                        data = await response.json()
                    except Exception:
                        text = await response.text()
                        print(f"Не JSON-ответ от /category! raw: {text}")
                        return ['unknown']
                    if 'category' not in data:
                        print(f"В ответе /category нет ключа category! data: {data}")
                        return ['unknown']
                    return [data['category']]

        if not api_key:
            return ['unknown', 'OpenAI API key not found!']

        try:
            client = OpenAI(api_key=api_key)
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
            return [response.choices[0].message.content.strip()]
        except Exception as e:
            return [f"OpenAI API error: {e}", 'unknown']



CATEGORIZE = Categorize()