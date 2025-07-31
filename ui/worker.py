import asyncio
import os
from dotenv import load_dotenv
from temporalio.client import Client
from temporalio.worker import Worker
from temporal_workflow import OllamaWorkflow, get_ollama_response

# Load environment variables from .env file
load_dotenv()

TEMPORAL_TASK_QUEUE = os.getenv("TEMPORAL_TASK_QUEUE", "ollama-task-queue")
TEMPORAL_HOST = os.getenv("TEMPORAL_HOST", "localhost")

async def main():
    client = await Client.connect(f"{TEMPORAL_HOST}:7233")
    worker = Worker(
        client,
        task_queue=TEMPORAL_TASK_QUEUE,
        workflows=[OllamaWorkflow],
        activities=[get_ollama_response],
    )
    await worker.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker gracefully shut down.")