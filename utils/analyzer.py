from .skills_db import skills_list, skill_aliases
from .job_roles import job_roles


def normalize_text(text: str):
    text = text.lower()

    # replace aliases
    for alias, real in skill_aliases.items():
        text = text.replace(alias, real)

    return text


def extract_skills(text: str):
    text = normalize_text(text)

    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


def suggest_roles(input_role: str):
    suggestions = []

    for role in job_roles.keys():
        if input_role in role:
            suggestions.append(role)

    return suggestions


def match_job_role(skills, role):
    role = role.lower()

    if role not in job_roles:
        return {
            "role": role,
            "error": "Role not found",
            "available_roles": list(job_roles.keys()),
            "suggestions": suggest_roles(role)
        }

    role_data = job_roles[role]
    required = role_data["required"]
    optional = role_data["optional"]

    matched_required = [s for s in skills if s in required]
    matched_optional = [s for s in skills if s in optional]

    missing_required = [s for s in required if s not in skills]

    score = (len(matched_required) * 10) + (len(matched_optional) * 5)
    max_score = (len(required) * 10) + (len(optional) * 5)

    match_percent = int((score / max_score) * 100)

    if match_percent < 40:
        level = "Beginner"
    elif match_percent < 70:
        level = "Intermediate"
    else:
        level = "Strong"

    recommendations = []

    for skill in missing_required:
        recommendations.append(f"Learn {skill} to improve your profile")

    if match_percent < 50:
        recommendations.append("Focus on core skills before applying")

    if "projects" not in skills:
        recommendations.append("Build 2-3 real-world projects")

    return {
        "role": role,
        "match_percentage": match_percent,
        "level": level,
        "matched_required_skills": matched_required,
        "matched_optional_skills": matched_optional,
        "missing_skills": missing_required,
        "recommendations": recommendations
    }