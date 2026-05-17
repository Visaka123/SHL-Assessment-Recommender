from app.retrieval.hybrid_search import (
    hybrid_search
)

from app.llm.client import (
    generate_response
)

from app.llm.prompts import (
    SYSTEM_PROMPT
)


def compare_assessments(query):

    results = hybrid_search(
        query,
        top_k=2
    )

    context = ""

    for item in results:

        context += f"""
        Name: {item['name']}
        Description: {item['description']}
        Test Type: {item['test_type']}
        """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"""
            Compare these SHL assessments.

            Context:
            {context}

            User query:
            {query}
            """
        }
    ]

    return generate_response(messages)