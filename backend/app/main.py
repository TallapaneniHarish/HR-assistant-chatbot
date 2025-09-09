# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Any

from search_engine import get_searcher
from employees_data import employees

app = FastAPI(title="HR Finder Chatbot API", version="1.0")

searcher = get_searcher()

class ChatRequest(BaseModel):
    query: str
    k: Optional[int] = 5
    # optional: enable_llm to generate richer text via external LLM if configured later
    enable_llm: Optional[bool] = False

class EmployeeSearchResponse(BaseModel):
    id: int
    name: str
    skills: List[str]
    experience_years: int
    projects: List[str]
    availability: str
    score: Optional[float] = None
    notes: Optional[str] = None

class ChatResponse(BaseModel):
    response_text: str
    candidates: List[EmployeeSearchResponse]

@app.get("/employees/search", response_model=List[EmployeeSearchResponse])
def employees_search(query: str, k: int = 5):
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")
    results = searcher.search(query, k=k)
    out = []
    for r in results:
        emp = r["employee"]
        out.append(EmployeeSearchResponse(
            id=emp["id"],
            name=emp["name"],
            skills=emp["skills"],
            experience_years=emp["experience_years"],
            projects=emp["projects"],
            availability=emp["availability"],
            score=round(r.get("score", 0), 4),
            notes=emp.get("notes","")
        ))
    return out

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")
    k = req.k or 5
    candidates = searcher.search(req.query, k=k)
    # For now we use template-based generation. If enable_llm is true and you have OpenAI key,
    # you can add code here to call an LLM to produce a richer narrative.
    response_text = searcher.generate_response(req.query, candidates)
    # build candidate summary in response model
    cands = []
    for r in candidates:
        emp = r["employee"]
        cands.append(EmployeeSearchResponse(
            id=emp["id"],
            name=emp["name"],
            skills=emp["skills"],
            experience_years=emp["experience_years"],
            projects=emp["projects"],
            availability=emp["availability"],
            score=round(r.get("score", 0), 4),
            notes=emp.get("notes","")
        ))
    return ChatResponse(response_text=response_text, candidates=cands)

# Root health check
@app.get("/")
def read_root():
    return {"message":"HR Finder Chatbot API is running. Use /docs for API UI."}
