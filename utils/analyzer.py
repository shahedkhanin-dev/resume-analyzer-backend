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
    normalized_role = role.lower().strip()

    matched_key = None

    for key in job_roles:
        if normalized_role in key:
            matched_key = key
            break

    if not matched_key:
        return {
            "error": "Role not found",
            "available_roles": list(job_roles.keys())
        }

    required = job_roles[matched_key]

    matched = [skill for skill in skills if skill in required]
    missing = [skill for skill in required if skill not in skills]

    match_percent = int((len(matched) / len(required)) * 100)

    return {
        "role": matched_key,
        "match_percentage": match_percent,
        "matched_skills": matched,
        "missing_skills": missing
    }