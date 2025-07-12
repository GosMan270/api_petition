from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from datetime import datetime
from fastapi import Query
from typing import List, Optional

from app.database import DATABASE
from app.sentiment import SENTIMENT
from app.categorize import CATEGORIZE

app = FastAPI()


class ComplaintIn(BaseModel):
    text: str


class ComplaintClose(BaseModel):
    id: int

class ComplaintOut(BaseModel):
    id: int
    text: str
    status: str
    sentiment: str
    category: str

class ComplaintStatusUpdate(BaseModel):
    status: str

@app.on_event("startup")
async def startup():
    await DATABASE.open_connection("database.sqlite")

@app.on_event("shutdown")
async def shutdown():
    await DATABASE.close_connection()

@app.post("/complaints", response_model=ComplaintOut, response_model_exclude_none=True)
async def add_complaint(complaint: ComplaintIn):
    status = "open"
    sentiment = await SENTIMENT.analyze_text(complaint.text)
    category = await CATEGORIZE.OpenAi(complaint.text)

    sentiment_value = sentiment[0]
    category_value = category[0]

    ts = datetime.utcnow().isoformat()
    # Предполагаем, что add_other возвращает id вставленной записи
    await DATABASE.add_other(complaint.text, status, ts, sentiment_value, category_value)
    id = DATABASE.last_id

    return ComplaintOut(
        id=id,
        text=complaint.text,
        status=status,
        sentiment=sentiment_value,
        category=category_value
    )


@app.post("/close")
async def close_complaint(complaint: ComplaintClose):
    await DATABASE.update_status(complaint.id, 'close')
    print({"message": f"Жалоба {complaint.id} закрыта."})
    return True


@app.get("/complaints", response_model=List[ComplaintOut])
async def get_complaints(
    status: Optional[str] = Query(None),
    timestamp: Optional[str] = Query(None)
):
    ts = None
    if timestamp is not None:
        ts = datetime.fromisoformat(timestamp.replace("Z", ""))  # если приходит с Z на конце
    rows = await DATABASE.get_complaints_filtered(status=status, since=ts)

    # Порядок соответствующий таблице complaints (id, text, status, timestamp, sentiment, category, ip)
    return [
        ComplaintOut(
            id=row[0],
            text=row[1],
            status=row[2],
            sentiment=row[4],
            category=row[5]
        )
        for row in rows
    ]


@app.patch("/complaints/{complaint_id}", response_model=ComplaintOut)
async def update_complaint_status(
    complaint_id: int,
    update: ComplaintStatusUpdate
):
    # 1. Обновление статуса
    await DATABASE.update_status(complaint_id, update.status)
    # 2. Выборка обновлённой жалобы
    rows = await DATABASE.get_complaints_filtered()
    complaint_row = next((row for row in rows if row[0] == complaint_id), None)
    if not complaint_row:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return ComplaintOut(
        id=complaint_row[0],
        status=complaint_row[2],
        sentiment=complaint_row[4],
        category=complaint_row[5]
    )