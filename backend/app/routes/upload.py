from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.services.resume_parser import extract_resume_text
from app.services.skill_extractor import extract_skills

from app.database import SessionLocal
from app.models.resume import Resume

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):

    file_location = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        

    resume_text = extract_resume_text(file_location)
    skills = extract_skills(resume_text)

    # ===== ATS SCORE CALCULATION =====

    skill_score = min(len(skills) * 5, 40)

    text_length_score = 20 if len(resume_text) > 500 else 10

    sections = ["education", "project", "experience", "skills"]
    section_score = sum(
        1 for s in sections if s in resume_text.lower()
    ) / len(sections) * 20

    keyword_score = min(len(skills) / 15, 1) * 20

    ats_score = skill_score + text_length_score + section_score + keyword_score

    # ===== PENALTIES =====
    penalty = 0

    if "project" not in resume_text.lower():
        penalty += 10

    if "experience" not in resume_text.lower():
        penalty += 10

    if len(resume_text) < 400:
        penalty += 10

    if len(skills) > 15:
        penalty += 5

    ats_score = ats_score - penalty

    # Clamp score
    # Normalize score to realistic ATS range

    # Reduce high scores
    if ats_score > 85:
        ats_score = 85 + (ats_score - 85) * 0.3

    # Reduce mid scores slightly
    elif ats_score > 70:
        ats_score = 70 + (ats_score - 70) * 0.7

    # Clamp between 30–92
    ats_score = max(30, min(ats_score, 92))

    ats_score = round(ats_score, 2)

    # ===== SAVE TO DB =====
    db = SessionLocal()

    new_resume = Resume(
        filename=file.filename,
        skills=", ".join(skills),
        ats_score=ats_score,
        resume_text=resume_text
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {
        "filename": file.filename,
        "skills": skills,
        "ats_score": ats_score,
        "id": new_resume.id
    }