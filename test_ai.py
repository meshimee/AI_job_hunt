from app.ai.ollama_client import ask_ai


prompt = """
You are JobHunt AI, an AI employee that manages a person's job search.

Introduce yourself in 5 short bullet points.
"""

answer = ask_ai(prompt)

print("\n--- JOBHUNT AI ---\n")
print(answer)