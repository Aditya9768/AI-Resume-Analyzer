from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import upload
from app.database import engine
from app.models import resume
from app.routes import job_match
from app.routes import report

resume.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(job_match.router)
app.include_router(report.router)


@app.get("/")
def read_root():
    return {"message": "AI Resume Analyzer Backend Running"}