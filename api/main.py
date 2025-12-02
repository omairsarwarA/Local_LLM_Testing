from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from llm_service import LocalLLM
from .db import SessionLocal, engine, Base
from .models import ChatHistory
from .exporter import export_to_json, export_to_excel

Base.metadata.create_all(bind=engine)

app = FastAPI()
llm = LocalLLM("gemma3:1b")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/chat")
def chat(prompt: str, db: Session = Depends(get_db)):
    resp = llm.ask(prompt)
    chat_entry = ChatHistory(query=prompt, response=resp)
    db.add(chat_entry)
    db.commit()
    db.refresh(chat_entry)
    return {"id": chat_entry.id, "query": prompt, "response": resp}

@app.get("/history")
def history(db: Session = Depends(get_db)):
    return db.query(ChatHistory).order_by(ChatHistory.created_at.desc()).all()

@app.get("/export/json")
def export_json(db: Session = Depends(get_db)):
    records = [{"query": c.query, "response": c.response, "created_at": c.created_at.isoformat()} 
               for c in db.query(ChatHistory).all()]
    export_to_json(records)
    return {"status": "success", "file": "chat_history.json"}

@app.get("/export/excel")
def export_excel(db: Session = Depends(get_db)):
    records = [{"query": c.query, "response": c.response, "created_at": c.created_at.isoformat()} 
               for c in db.query(ChatHistory).all()]
    export_to_excel(records)
    return {"status": "success", "file": "chat_history.xlsx"}
