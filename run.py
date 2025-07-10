from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.database import DATABASE
from app.sentiment import SENTIMENT
from app.categorize import CATEGORIZE
app = FastAPI()

class ComplaintIn(BaseModel):
    text: str

class ComplaintOut(BaseModel):
    id: int
    status: str
    sentiment: str
    category: str

@app.on_event("startup")
async def startup():
    await DATABASE.open_connection("database.sqlite")

@app.on_event("shutdown")
async def shutdown():
    await DATABASE.close_connection()

@app.post("/complaints", response_model=ComplaintOut, response_model_exclude_none=True)
async def add_complaint(complaint: ComplaintIn):
    status = "open"
    sentiment = str(await SENTIMENT.analyze_text(complaint.text))
    print(sentiment[1])
    category = str(CATEGORIZE.OpenAi(complaint.text))
    print(category)
    ts = datetime.utcnow().isoformat()
    await DATABASE.add_other(complaint.text, status, ts, sentiment, category)
    id = DATABASE.last_id

    return ComplaintOut(
        id=id,
        status=status,
        sentiment=sentiment[1],
        category=category[0],
    )

