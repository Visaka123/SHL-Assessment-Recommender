def needs_clarification(constraints):

    role = constraints.get(
        "role"
    )

    skills = constraints.get(
        "skills",
        []
    )

    seniority = constraints.get(
        "seniority"
    )

    # If absolutely nothing useful
    if (
        not role
        and not skills
        and not seniority
    ):
        return True

    # If role exists but no skills,
    # still continue
    # Example:
    # "Need assessment for Java developer"

    return False