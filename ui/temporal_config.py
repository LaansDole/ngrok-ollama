import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Temporal configuration
    TEMPORAL_HOST = os.getenv("TEMPORAL_HOST", "localhost")
    TEMPORAL_PORT = os.getenv("TEMPORAL_PORT", "7233")
    TEMPORAL_TASK_QUEUE = os.getenv("TEMPORAL_TASK_QUEUE", "ollama-task-queue")
    
    # Ollama configuration
    OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/chat")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama2")

# Global config instance
config = Config()
