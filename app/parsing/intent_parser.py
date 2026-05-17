
SKILL_KEYWORDS = [
    "java",
    "python",
    "sql",
    "javascript",
    "react",
    "node",
    "communication",
    "stakeholder",
    "leadership"
]


def extract_constraints(query):

    query = query.lower()

    skills = []

    for skill in SKILL_KEYWORDS:

        if skill in query:
            skills.append(skill)

    return {
        "skills": skills,
        "leadership": (
            "leadership" in query
            or "executive" in query
            or "director" in query
        ),
        "personality_required": (
            "communication" in query
            or "stakeholder" in query
            or "personality" in query
        )
    }