from app.services.skill_extractor import extract_skills


def match_resume_with_job(resume_text, job_description):

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched = list(set(resume_skills).intersection(set(job_skills)))
    missing = list(set(job_skills) - set(resume_skills))

    skill_comparison = []

    for skill in job_skills:

        if skill in resume_skills:
            value = 100
        else:
            value = 0

        skill_comparison.append({
            "skill": skill,
            "score": value
        })

    if len(job_skills) == 0:
        match_score = 0
    else:
        match_score = (len(matched) / len(job_skills)) * 100

    return {
        "match_score": round(match_score, 2),
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_chart": skill_comparison
    }