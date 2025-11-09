import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from typing import List

from database import db, create_document, get_documents
from schemas import Project, Skill, Message

app = FastAPI(title="Portfolio API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Portfolio Backend Running"}


@app.get("/test")
def test_database():
    """Quick health check for backend and database connectivity"""
    status = {
        "backend": "ok",
        "database": "disconnected",
        "collections": [],
    }
    try:
        if db is not None:
            status["database"] = "connected"
            try:
                status["collections"] = db.list_collection_names()[:10]
            except Exception:
                pass
    except Exception as e:
        status["error"] = str(e)
    return status


# ---------- Public Content Endpoints ----------

@app.get("/api/projects", response_model=List[Project])
def get_projects():
    try:
        docs = get_documents("project")
        # sanitize _id for response by mapping to string or dropping
        projects = []
        for d in docs:
            d.pop("_id", None)
            projects.append(Project(**d))
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/skills", response_model=List[Skill])
def get_skills():
    try:
        docs = get_documents("skill")
        skills: List[Skill] = []
        for d in docs:
            d.pop("_id", None)
            skills.append(Skill(**d))
        return skills
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- Contact Endpoint ----------

@app.post("/api/contact")
def submit_contact(payload: Message):
    try:
        # Validate via Pydantic and store the message
        doc_id = create_document("message", payload)
        return {"status": "ok", "id": doc_id}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
