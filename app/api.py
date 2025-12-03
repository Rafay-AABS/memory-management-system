# app/api.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from .composer import process_input
from . import strings

app = FastAPI(title="Memory Management System API")

class HistoryItem(BaseModel):
    role: str
    query: str
    timestamp: str

class CurrentItem(BaseModel):
    role: str
    query: str
    timestamp: str

class InputModel(BaseModel):
    input: str
    current: CurrentItem
    history: List[HistoryItem]

@app.post("/process")
def process_endpoint(payload: InputModel):
    payload_dict = payload.dict()
    result = process_input(payload_dict)
    return result
