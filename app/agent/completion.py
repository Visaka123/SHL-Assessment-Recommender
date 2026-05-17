COMPLETION_PHRASES = [
    "perfect",
    "that's what we need",
    "thanks",
    "great",
    "looks good"
]


def is_conversation_complete(messages):

    last_user = None

    for msg in reversed(messages):

        if msg["role"] == "user":
            last_user = msg["content"].lower()
            break

    if not last_user:
        return False

    return any(
        phrase in last_user
        for phrase in COMPLETION_PHRASES
    )