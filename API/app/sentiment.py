"""
Module for analyzing sentiment using APILayer or a test endpoint.
"""

import os
from typing import List
import aiohttp
from dotenv import load_dotenv


class Sentiment:
    """
    Service for analyzing sentiment using APILayer or a mock endpoint.
    """
    def __init__(self):
        self.dotenv_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config.env'
        )
        load_dotenv(self.dotenv_path)

    async def api_layer(self, message: str) -> List[str]:
        """
        Analyze sentiment of a message using APILayer or test API.
        """
        url = "https://api.apilayer.com/sentiment/analysis"
        test_mode = bool(os.getenv('Test_Mode'))
        payload = message.encode("utf-8")
        headers = {"apikey": os.getenv('API_LAYER_KEY')}

        if test_mode:
            url = 'http://fastapi_test:7000/sentiment'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    try:
                        data = await response.json()
                    except Exception:  # Можно заменить на конкретную ошибку
                        text = await response.text()
                        print(f"Non-JSON response from /sentiment! raw: {text}")
                        return ['unknown']
                    if 'sentiment' not in data:
                        print(f"No 'sentiment' key in response; data: {data}")
                        return ['unknown']
                    return [data['sentiment']]

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                result = []
                data = await response.json()

                if response.status != 200:
                    result.append(f"Request status code: {response.status}")
                    result.append('unknown')
                else:
                    sentiment_analysis = data.get('sentiment', 'unknown')
                    result.append(f"Request status code: {response.status}")
                    result.append(sentiment_analysis)

                return result

    async def analyze_text(self, text: str) -> List[str]:
        """
        Analyze text and return the sentiment result.
        """
        result = await self.api_layer(text)
        return result


SENTIMENT = Sentiment()
