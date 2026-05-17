def needs_clarification(state):

    # extremely vague
    if (
        not state["leadership"]
        and not state["skills"]
    ):
        return (
            True,
            "What role or job family are you hiring for?"
        )

    # leadership but no seniority
    if (
        state["leadership"]
        and not state["seniority"]
    ):
        return (
            True,
            "Who is this meant for?"
        )

    # leadership but no use-case
    if (
        state["leadership"]
        and not state["selection"]
        and not state["development"]
    ):
        return (
            True,
            "Is this for selection or development?"
        )

    return (False, None)