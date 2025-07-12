"""
Main application module for the Complaints API.
Provides endpoints for creating, listing, updating, and closing complaints.
"""

from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app.database import DATABASE
from app.sentiment import SENTIMENT
from app.categorize import CATEGORIZE

app = FastAPI()


class ComplaintIn(BaseModel):
    """
    Model for incoming complaint.
    """
    text: str


class ComplaintClose(BaseModel):
    """
    Model for closing a complaint.
    """
    complaint_id: int  # PEP8: use a name that does not shadow built-ins


class ComplaintOut(BaseModel):
    """
    Model for returning complaint info.
    """
    complaint_id: int
    text: str
    status: str
    sentiment: str
    category: str


class ComplaintStatusUpdate(BaseModel):
    """
    Model for updating complaint status.
    """
    status: str


@app.on_event("startup")
async def startup():
    """Initialize database connection on startup."""
    await DATABASE.open_connection("database.sqlite")


@app.on_event("shutdown")
async def shutdown():
    """Close database connection on shutdown."""
    await DATABASE.close_connection()


@app.post("/complaints", response_model=ComplaintOut, response_model_exclude_none=True)
async def add_complaint(complaint: ComplaintIn):
    """
    Create a new complaint, analyze its sentiment and category.
    """
    status = "open"
    sentiment = await SENTIMENT.analyze_text(complaint.text)
    category = await CATEGORIZE.OpenAi(complaint.text)

    sentiment_value = sentiment[0]
    category_value = category[0]

    timestamp = datetime.utcnow().isoformat()
    await DATABASE.add_other(complaint.text, status, timestamp, sentiment_value, category_value)
    complaint_id = DATABASE.last_id

    return ComplaintOut(
        complaint_id=complaint_id,
        text=complaint.text,
        status=status,
        sentiment=sentiment_value,
        category=category_value
    )


@app.post("/close")
async def close_complaint(complaint: ComplaintClose):
    """
    Mark a complaint as closed.
    """
    await DATABASE.update_status(complaint.complaint_id, 'close')
    print({"message": f"Жалоба {complaint.complaint_id} закрыта."})
    return True


@app.get("/complaints", response_model=List[ComplaintOut])
async def get_complaints(
    status: Optional[str] = Query(default=None),
    timestamp: Optional[str] = Query(default=None)
):
    """
    Get a list of complaints with optional filtering by status and timestamp.
    """
    ts = None
    if timestamp is not None:
        ts = datetime.fromisoformat(timestamp.replace("Z", ""))  # если приходит с Z на конце
    rows = await DATABASE.get_complaints_filtered(status=status, since=ts)

    return [
        ComplaintOut(
            complaint_id=row[0],
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
    """
    Update status of a single complaint by id.
    """
    await DATABASE.update_status(complaint_id, update.status)
    rows = await DATABASE.get_complaints_filtered()
    complaint_row = next((row for row in rows if row[0] == complaint_id), None)
    if not complaint_row:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return ComplaintOut(
        complaint_id=complaint_row[0],
        text=complaint_row[1],
        status=complaint_row[2],
        sentiment=complaint_row[4],
        category=complaint_row[5]
    )