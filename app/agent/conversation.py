LEADERSHIP_KEYWORDS = [
    "leadership",
    "cxo",
    "director",
    "executive",
    "vp",
    "senior leadership"
]

PERSONALITY_KEYWORDS = [
    "personality",
    "behavior",
    "behaviour",
    "opq"
]

SELECTION_KEYWORDS = [
    "selection",
    "benchmark",
    "hiring"
]

DEVELOPMENT_KEYWORDS = [
    "development",
    "coaching",
    "feedback"
]


def reconstruct_state(messages):

    state = {
        "skills": [],
        "seniority": None,
        "leadership": False,
        "personality_required": False,
        "selection": False,
        "development": False,
        "role": None
    }

    for msg in messages:

        if msg.role != "user":
            continue

        text = msg.content.lower()

        # leadership
        if any(k in text for k in LEADERSHIP_KEYWORDS):
            state["leadership"] = True

        # personality
        if any(k in text for k in PERSONALITY_KEYWORDS):
            state["personality_required"] = True

        # selection
        if any(k in text for k in SELECTION_KEYWORDS):
            state["selection"] = True

        # development
        if any(k in text for k in DEVELOPMENT_KEYWORDS):
            state["development"] = True

        # seniority
        if (
            "15 years" in text
            or "cxo" in text
            or "director" in text
        ):
            state["seniority"] = "senior"

        elif (
            "mid" in text
            or "4 years" in text
        ):
            state["seniority"] = "mid"

        elif (
            "entry" in text
            or "junior" in text
        ):
            state["seniority"] = "junior"

    return state


def build_conversation_context(messages):

    combined = []
    latest_user = ""

    for msg in messages:

        role = msg.role.upper()
        content = msg.content

        combined.append(f"{role}: {content}")

        if msg.role == "user":
            latest_user = msg.content

    return {
        "conversation_text": "\n".join(combined),
        "latest_user_message": latest_user,
        "combined_query": latest_user
    }