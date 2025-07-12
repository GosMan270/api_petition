"""
Mock API for simulating category and sentiment endpoints.
Used in test mode.
"""

import random
from fastapi import FastAPI

app = FastAPI()


@app.get("/category")
def get_category():
    """
    Return a random complaint category for testing.
    """
    return {"category": random.choice(["платежи", "техническая", "другое"])}


@app.get("/sentiment")
def get_sentiment():
    """
    Return a random sentiment for testing.
    """
    return {"sentiment": random.choice(["позитивная", "нейтральная", "негативная"])}
