import os
import aiohttp
import asyncio

from dotenv import load_dotenv


class Sentiment:
    def __init__(self):
        self.dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.env')
        self.dotenv = load_dotenv(self.dotenv_path)


    async def APILayer(self, message):
        url = "https://api.apilayer.com/sentiment/analysis"

        payload = f"{message}".encode("utf-8")
        headers = {"apikey": f"{os.getenv("API_LAYER_KEY")}"}
        print(headers)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                res = response.status
                data = await response.json()
                print(res)
                print(data)

            if res != 200:
                return 'unknown'
            else:
                return data


SENTIMENT = Sentiment()





