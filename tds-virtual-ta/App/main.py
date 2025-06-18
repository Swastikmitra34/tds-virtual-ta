from fastapi import FastAPI
from pydantic import BaseModel
from App.rag import query

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    image: str = None  

@app.post("/api/")
def ask_virtual_ta(req: QuestionRequest):
    result = query(req.question)
    return result
