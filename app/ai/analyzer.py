import json
import re

from app.ai.ollama_client import ask_ai


def analyze_job_description(job_description: str) -> dict:
    """
    Analyze a job description using the local Ollama model.
    """

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    prompt = f"""
Analyze this job description and return ONLY valid JSON.

Use exactly this structure:

{{
    "job_title": "",
    "experience_required": "",
    "education_required": "",
    "employment_type": "",
    "location": "",
    "required_skills": [],
    "preferred_skills": [],
    "technical_skills": [],
    "soft_skills": [],
    "responsibilities": [],
    "domain": [],
    "keywords": [],
    "certifications": [],
    "summary": ""
}}

Rules:

- Do not invent information.
- required_skills = explicitly required skills.
- preferred_skills = preferred or nice-to-have skills.
- technical_skills = programming languages, frameworks,
  databases, APIs, cloud technologies, security technologies,
  tools and other technical technologies.
- soft_skills = communication, teamwork, leadership,
  stakeholder management, analytical thinking and problem solving.
- responsibilities = concise list of main responsibilities.
- domain = industries or business areas.
- keywords = important job and ATS keywords.
- certifications = certifications explicitly mentioned.
- summary = maximum 2 sentences.
- Use empty strings or [] when information is unavailable.

JOB DESCRIPTION:

{job_description}
"""

    raw_response = ask_ai(prompt)

    return _parse_json_response(raw_response)


def _parse_json_response(response: str) -> dict:
    """
    Convert the AI response into a Python dictionary.
    """

    response = response.strip()

    # Remove markdown code fences if the model returns them
    response = re.sub(
        r"^```json\s*",
        "",
        response,
        flags=re.IGNORECASE
    )

    response = re.sub(
        r"^```\s*",
        "",
        response
    )

    response = re.sub(
        r"\s*```$",
        "",
        response
    )

    try:
        data = json.loads(response)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"AI returned invalid JSON.\n\n"
            f"AI Response:\n{response}"
        ) from error

    if not isinstance(data, dict):
        raise ValueError(
            "AI response must be a JSON object."
        )

    return data


def analyze_job_from_text(job_description: str) -> None:
    """
    Analyze a job description and print the result.
    """

    analysis = analyze_job_description(job_description)

    print(
        json.dumps(
            analysis,
            indent=4,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":

    sample_job = """
    We are looking for a Digital Transformation Analyst
    with 2-4 years of experience in banking or financial services.

    The candidate should have experience with Java, SQL,
    Spring Boot, REST APIs and application support.

    Knowledge of cloud technologies, Agile methodology and
    cybersecurity is preferred.

    Responsibilities include gathering business requirements,
    coordinating with development teams, supporting banking
    applications, analyzing issues and assisting with
    digital transformation initiatives.

    Bachelor's degree in Computer Science or a related field
    is required.
    """

    analyze_job_from_text(sample_job)