def calculate_ats_score(resume_skills, job_skills, text):

    matched = len(set(resume_skills) & set(job_skills))
    total_job = len(job_skills)

    # Skill match (40%)
    skill_score = (matched / total_job) * 40 if total_job else 0

    # Resume coverage (20%)
    coverage = (matched / len(resume_skills)) * 20 if resume_skills else 0

    # Keyword density (15%)
    keyword_density = min(len(resume_skills) / 20, 1) * 15

    # Section presence (15%)
    sections = ["education", "project", "experience", "skills"]
    section_score = sum(1 for s in sections if s in text.lower()) / len(sections) * 15

    # Quality (10%)
    quality_score = 10 if len(text) > 500 else 5

    total_score = skill_score + coverage + keyword_density + section_score + quality_score

    return round(total_score, 2)