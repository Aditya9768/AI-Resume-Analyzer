from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.database import SessionLocal
from app.models.resume import Resume
from app.services.report_generator import generate_report

router = APIRouter()


@router.get("/download-report/{resume_id}")
def download_report(resume_id: int):

    db = SessionLocal()

    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        return {"error": "Resume not found"}

    skills = resume.skills.split(",")

    file_path = generate_report(
        resume.filename,
        skills,
        resume.ats_score
    )

    return FileResponse(file_path, media_type='application/pdf', filename="analysis_report.pdf")