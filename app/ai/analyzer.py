import json
import re

from app.ai.ollama_client import ask_ai


def analyze_job_description(job_description: str) -> dict:
    """
    Analyze a job description using the local Ollama model.

    Returns structured information about the job.
    """

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    prompt = f"""
You are an expert technical recruiter and job description analyzer.

Analyze the following job description.

Return ONLY valid JSON.
Do not include markdown.
Do not include ```json.
Do not add explanations outside the JSON.

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

1. Extract only information supported by the job description.
2. Do not invent skills or requirements.
3. If information is missing, use an empty string or empty list.
4. Keep skills as concise names.
5. Separate required skills from preferred skills.
6. Identify the business/industry domain.
7. Extract important ATS keywords.
8. Keep responsibilities concise.
9. The final response must be valid JSON.

JOB DESCRIPTION:

{job_description}
"""

    raw_response = ask_ai(prompt)

    return _parse_json_response(raw_response)


def _parse_json_response(response: str) -> dict:
    """
    Convert the AI response into a Python dictionary.

    Handles cases where the model accidentally returns
    markdown code fences around the JSON.
    """

    response = response.strip()

    # Remove markdown code fences if Ollama returns them
    response = re.sub(r"^```json\s*", "", response, flags=re.IGNORECASE)
    response = re.sub(r"^```\s*", "", response)
    response = re.sub(r"\s*```$", "", response)

    try:
        data = json.loads(response)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"AI returned invalid JSON.\n\nAI Response:\n{response}"
        ) from error

    if not isinstance(data, dict):
        raise ValueError("AI response must be a JSON object.")

    return data


def analyze_job_from_text(job_description: str) -> None:
    """
    Analyze a job description and print the result.

    Useful for testing from the command line.
    """

    analysis = analyze_job_description(job_description)

    print(json.dumps(analysis, indent=4, ensure_ascii=False))


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