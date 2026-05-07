from fastapi import APIRouter

from app.services.job_matcher import match_resume_with_job
from app.database import SessionLocal
from app.models.resume import Resume

router = APIRouter()


@router.post("/match-job/")
def match_job(data: dict):

    resume_id = data.get("resume_id")
    job_description = data.get("job_description")

    db = SessionLocal()

    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        return {"error": "Resume not found"}

    result = match_resume_with_job(resume.resume_text, job_description)

    return result