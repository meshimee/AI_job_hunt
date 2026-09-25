import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def ask_ai(prompt: str) -> str:
    """Send a prompt to local Ollama and return its response."""

    print("Sending request to Ollama...")

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0,
                    "num_predict": 500
                }
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        print("Ollama response received.")

        return data["response"]

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Ollama took too long to generate the response."
        )

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not connect to Ollama at http://localhost:11434."
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Ollama API request failed: {error}"
        )