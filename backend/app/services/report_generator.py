from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_report(filename, skills, ats_score):

    file_path = f"uploads/{filename}_report.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)

    c.drawString(100, 750, "AI Resume Analysis Report")

    c.drawString(100, 720, f"Resume File: {filename}")

    c.drawString(100, 690, f"ATS Score: {ats_score}")

    y = 650

    c.drawString(100, y, "Detected Skills:")

    y -= 20

    for skill in skills:
        c.drawString(120, y, f"- {skill}")
        y -= 20

    c.save()

    return file_path