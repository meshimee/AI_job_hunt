import json

from app.ai.ollama_client import ask_ai
from app.database.database import get_connection


HIRING_POST = """
We are hiring!

Company: NovaTech

Role: Business Operations Associate

We are looking for someone who can support business operations,
analyze business data, coordinate with different teams, and help
improve operational processes.

Location: Bangalore

If interested, please send your CV to the recruiting team.
"""


def extract_opportunity(post):
    prompt = f"""
You are an information extraction system for a job-search application.

Read the hiring post below and extract the information into JSON.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations.

Use exactly these fields:

{{
    "company": "",
    "role": "",
    "contact_name": "",
    "contact_role": "",
    "source": "Hiring Post",
    "stage": "Potential",
    "status": "New",
    "priority": "",
    "deadline": "",
    "next_action": "",
    "notes": ""
}}

Hiring post:

{post}
"""

    response = ask_ai(prompt)

    # Remove accidental markdown code fences
    response = response.replace("```json", "").replace("```", "").strip()

    return json.loads(response)


def save_opportunity(opportunity):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO opportunities (
            company,
            role,
            contact_name,
            contact_role,
            source,
            stage,
            status,
            priority,
            deadline,
            next_action,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            opportunity["company"],
            opportunity["role"],
            opportunity["contact_name"],
            opportunity["contact_role"],
            opportunity["source"],
            opportunity["stage"],
            opportunity["status"],
            opportunity["priority"],
            opportunity["deadline"],
            opportunity["next_action"],
            opportunity["notes"],
        ),
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    print("Analyzing hiring post...\n")

    opportunity = extract_opportunity(HIRING_POST)

    print("AI extracted:")
    print(json.dumps(opportunity, indent=2))

    save_opportunity(opportunity)

    print("\nOpportunity saved successfully.")