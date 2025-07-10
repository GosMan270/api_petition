import os
import aiohttp
import asyncio
from dotenv import load_dotenv

class Sentiment:
    def __init__(self):
        self.dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.env')
        load_dotenv(self.dotenv_path)  # исправлено: была лишняя запись self.dotenv = окончание в оригинале

    async def APILayer(self, message):
        url = "https://api.apilayer.com/sentiment/analysis"

        payload = f"{message}".encode("utf-8")
        headers = {"apikey": os.getenv('API_LAYER_KEY')}  # исправлено использования кавычек

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                result = []
                data = await response.json()

                if response.status != 200:
                    result.append(f"Request status code: {response.status}")
                    result.append('unknown')
                else:
                    result.append(f"Request status code: {response.status}")
                    # Извлечение значимой части анализа тональности
                    sentiment_analysis = data.get('sentiment', 'unknown')
                    result.append(sentiment_analysis)

                return result  # добавили возвращение результата

    async def analyze_text(self, text):
        result = await self.APILayer(text)
        return result


SENTIMENT = Sentiment()