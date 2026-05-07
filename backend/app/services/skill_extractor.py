import re
from rapidfuzz import fuzz

# ==============================
# SKILLS DATABASE
# ==============================
SKILLS_DB = [
    "python","java","javascript","react","node","nodejs",
    "mongodb","sql","mysql","postgresql",
    "html","css","git","docker","kubernetes",
    "aws","azure","gcp",
    "machine learning","deep learning","data science",
    "django","flask","fastapi",
    "c++","c#","typescript","angular",

    # QA
    "testing","qa","manual testing",
    "automation testing","selenium",
    "jira","bug tracking","quality assurance"
]

# ==============================
# SYNONYMS
# ==============================
SKILL_MAP = {
    "javascript": ["js"],
    "react": ["reactjs"],
    "node": ["nodejs"],
    "mongodb": ["mongo"],
    "sql": ["database", "db"],

    "customer service": ["customer support", "client handling"],
    "communication": ["interaction"],
    "problem solving": ["issue resolution", "troubleshooting"]
}


# ==============================
# CLEAN TEXT (VERY IMPORTANT)
# ==============================
import re

def clean_text(text):
    # Lowercase everything
    text = text.lower()

    # Remove special chars, keep letters, numbers, +, #
    text = re.sub(r'[^a-zA-Z0-9+# ]', ' ', text)

    # Fix broken words like "p y t h o n" → "python"
    text = re.sub(
        r'(\b[a-z]\s+){3,}[a-z]\b',   # match sequences of single letters separated by spaces
        lambda x: x.group(0).replace(" ", ""),
        text
    )

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# ==============================
# MAIN FUNCTION
# ==============================
def extract_skills(text):

    text = clean_text(text)

    skill_counts = {}

    words = text.split()

    # -------------------------
    # STEP 1: EXACT MATCH
    # -------------------------
    for skill in SKILLS_DB:
        if skill in text:
            skill_counts[skill] = text.count(skill)

    # -------------------------
    # STEP 2: SYNONYM MATCH
    # -------------------------
    for skill, keywords in SKILL_MAP.items():
        if skill not in skill_counts:
            for keyword in keywords:
                if keyword in text:
                    skill_counts[skill] = 1
                    break

    # -------------------------
    # STEP 3: FUZZY MATCH
    # -------------------------
    for skill in SKILLS_DB:
        if skill not in skill_counts:
            for word in words:
                if fuzz.ratio(skill, word) > 85:
                    skill_counts[skill] = 1
                    break

    return skill_counts