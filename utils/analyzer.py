from .skills_db import skills_list
from .job_roles import job_roles


def extract_skills(text: str):
    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


def match_job_role(skills, role):
    role = role.lower().strip()

    role_map = {
        "frontend": "frontend developer",
        "backend": "backend developer",
        "data": "data scientist",
        "ml": "data scientist",
        "ai": "data scientist"
    }

    if role in role_map:
        role = role_map[role]

    if role not in job_roles:
        return {
            "role": role,
            "error": "Role not found",
            "available_roles": list(job_roles.keys())
        }

    required = job_roles[role]

    matched = [skill for skill in skills if skill in required]
    missing = [skill for skill in required if skill not in skills]

    match_percent = int((len(matched) / len(required)) * 100)

    # recommendations
    recommendations = []

    # always suggest improvement
    if match_percent >= 80:
        recommendations.append("Great profile! Try building advanced real-world projects")

    if "express" in missing:
        recommendations.append("Learn Express.js for backend development")

    if "node" in skills and "express" in missing:
        recommendations.append("Build REST APIs using Node.js + Express")

    if "mongodb" in skills:
        recommendations.append("Practice full-stack projects with MongoDB")

    if match_percent < 50:
        recommendations.append("Focus on core backend fundamentals")

    return {
        "role": role,
        "matched": matched,
        "missing": missing,
        "match_percent": match_percent,
        "recommendations": recommendations
    }