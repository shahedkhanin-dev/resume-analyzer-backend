from difflib import get_close_matches

ROLE_SKILLS = {
    "frontend developer": ["html", "css", "javascript", "react", "git"],
    "backend developer": ["python", "java", "node", "sql", "mongodb", "express"],
    "data scientist": ["python", "machine learning", "nlp", "pandas", "numpy"]
}

SKILL_WEIGHTS = {
    "javascript": 2,
    "react": 2,
    "python": 2,
    "machine learning": 3,
    "nlp": 3,
}

def extract_skills(text):
    text = text.lower()

    all_skills = set(sum(ROLE_SKILLS.values(), []))
    detected = [skill for skill in all_skills if skill in text]

    return list(set(detected))


def match_job_role(skills, role_input):
    role_input = role_input.lower()


    roles = list(ROLE_SKILLS.keys())
    matched_role = get_close_matches(role_input, roles, n=1, cutoff=0.5)

    if not matched_role:
        return {
            "role": role_input,
            "error": "Role not found",
            "available_roles": roles,
            "suggestions": get_close_matches(role_input, roles)
        }

    role = matched_role[0]
    required_skills = ROLE_SKILLS[role]

    score = 0
    total_weight = 0

    matched = []
    missing = []

    for skill in required_skills:
        weight = SKILL_WEIGHTS.get(skill, 1)
        total_weight += weight

        if skill in skills:
            score += weight
            matched.append(skill)
        else:
            missing.append(skill)

    match_percentage = int((score / total_weight) * 100)

    feedback = generate_feedback(role, matched, missing)

    recommendations = [
        f"Learn {skill} to improve your chances as a {role}"
        for skill in missing
    ]

    return {
        "role": role,
        "match_percentage": match_percentage,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": recommendations,
        "feedback": feedback
    }

def generate_feedback(role, matched, missing):
    if len(matched) > len(missing):
        return f"You have a strong foundation for a {role}. Focus on improving a few missing skills."

    elif len(matched) == 0:
        return f"Your resume does not currently align with {role}. Consider building relevant projects."

    else:
        return f"You partially match the {role} role. Strengthen your profile by learning {', '.join(missing[:2])}."