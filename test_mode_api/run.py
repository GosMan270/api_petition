from fastapi import FastAPI
import random


app = FastAPI()


@app.get("/category")
def get_category():
    return {"category": random.choice(["платежи", "техническая", "другое"])}


@app.get("/sentiment")
def get_sentiment():
    return {"sentiment": random.choice(["позитивная", "нейтральная", "негативная"])}