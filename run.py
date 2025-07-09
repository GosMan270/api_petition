from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from app.database import DATABASE
from app.sentiment import SENTIMENT
from app.categorize import CATEGORIZE
app = FastAPI()

class ComplaintIn(BaseModel):
    text: str

class ComplaintOut(BaseModel):
    id: int
    text: str
    status: str
    timestamp: str
    sentiment: str
    category: str

@app.on_event("startup")
async def startup():
    await DATABASE.open_connection("database.sqlite")

@app.on_event("shutdown")
async def shutdown():
    await DATABASE.close_connection()

@app.post("/complaints", response_model=ComplaintOut)
async def add_complaint(complaint: ComplaintIn):
    status = "open"
    sentiment = await SENTIMENT.APILayer(complaint.text)
    category = CATEGORIZE.OpenAi(complaint.text)
    ts = datetime.utcnow().isoformat()

    await DATABASE.add_other(complaint.text, status, ts, sentiment, category)
    id = DATABASE.last_id

    return ComplaintOut(
        id=id,
        text=complaint.text,
        status=status,
        timestamp=ts,
        sentiment=sentiment,
        category=category,
    )