from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2

from utils.analyzer import extract_skills, match_job_role

app = FastAPI()

# ✅ Add middleware RIGHT AFTER app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    role: str = Form(...)
):
    text = ""

    pdf = PyPDF2.PdfReader(file.file)

    for page in pdf.pages:
        text += page.extract_text()

    skills = extract_skills(text)

    result = match_job_role(skills, role)

    return {
        "skills_detected": skills,
        "analysis": result
    }