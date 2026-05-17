def rerank_results(results, constraints):

    if not results:
        return []

    role = constraints.get("role", "").lower()
    skills = [s.lower() for s in constraints.get("skills", [])]
    query = constraints.get("query", "").lower()

    ranked = []

    for item in results:

        score = item.get("score", 0)

        name = item.get("name", "").lower()
        description = item.get("description", "").lower()
        test_type = item.get("test_type", "").lower()

        combined = f"{name} {description} {test_type}"

        # ---------------- TECH BOOST ----------------
        tech_keywords = ["java", "developer", "software", "coding"]

        if any(k in query for k in tech_keywords):
            if any(k in combined for k in tech_keywords):
                score += 50

        # ---------------- COMMUNICATION BOOST ----------------
        comm_keywords = ["communication", "stakeholder", "collaboration"]

        if any(k in query for k in comm_keywords):
            if any(k in combined for k in comm_keywords):
                score += 30

        # ---------------- ROLE PENALTY ----------------
        if "java" in role:
            if ".net" in combined:
                score -= 80

        # ---------------- SKILL MATCH ----------------
        for skill in skills:
            if skill in combined:
                score += 25

        # ---------------- FINAL SAFE OUTPUT ----------------
        item["score"] = score

        # 🔥 CRITICAL FIX: NEVER LOSE URL
        if not item.get("url"):
            item["url"] = item.get("link", "")

        ranked.append(item)

    ranked.sort(key=lambda x: x["score"], reverse=True)

    # filter low quality
    return [r for r in ranked if r["score"] > 40][:10]