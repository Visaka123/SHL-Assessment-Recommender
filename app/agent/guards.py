OFFTOPIC_KEYWORDS = [
    "salary",
    "legal",
    "lawsuit",
    "movie",
    "weather",
    "hackerrank",
    "leetcode"
]

PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "system prompt",
    "bypass",
    "act as"
]


def is_offtopic(query: str):

    query = query.lower()

    return any(
        word in query
        for word in OFFTOPIC_KEYWORDS
    )


def is_prompt_injection(query: str):

    query = query.lower()

    return any(
        pattern in query
        for pattern in PROMPT_INJECTION_PATTERNS
    )