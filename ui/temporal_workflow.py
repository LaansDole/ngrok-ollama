
from dataclasses import dataclass
from datetime import timedelta
import os
from dotenv import load_dotenv
from temporalio import activity, workflow
import requests
import json

# Load environment variables from .env file
load_dotenv()

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/chat")

@dataclass
class OllamaInput:
    model: str
    messages: list

@activity.defn
async def get_ollama_response(input: OllamaInput) -> str:
    """Activity to get a response from the Ollama API."""
    full_response = ""
    try:
        data = {
            "model": input.model,
            "messages": input.messages,
            "stream": False,  # For simplicity in the activity, not streaming
        }
        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()
        json_response = response.json()
        if "message" in json_response and "content" in json_response["message"]:
            full_response = json_response["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except (json.JSONDecodeError, KeyError) as e:
        return f"Failed to parse response: {e}"
    return full_response

@workflow.defn
class OllamaWorkflow:
    @workflow.run
    async def run(self, model: str, messages: list) -> str:
        return await workflow.execute_activity(
            get_ollama_response,
            OllamaInput(model=model, messages=messages),
            start_to_close_timeout=timedelta(seconds=60),
        )
