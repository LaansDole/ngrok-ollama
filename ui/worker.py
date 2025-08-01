import asyncio
from temporalio.worker import Worker
from temporal_workflow import OllamaWorkflow, get_ollama_response
from temporal_manager import temporal_manager
from temporal_config import config
from logger import logger

async def main():
    try:
        client = await temporal_manager.get_client()
        if not client:
            logger.error("Failed to connect to Temporal, worker cannot start.")
            return

        # Test the connection by getting server info
        try:
            logger.info("Testing Temporal connection...")
            # Try to get cluster info to verify connection
            import temporalio.client
            await client.workflow_service.get_cluster_info(temporalio.api.workflowservice.v1.GetClusterInfoRequest())
            logger.info("Temporal connection test successful")
        except Exception as conn_test_error:
            logger.warning(f"Connection test warning: {conn_test_error}")

        logger.info(f"Starting worker with task queue: {config.TEMPORAL_TASK_QUEUE}")
        
        # Create worker with better error handling
        worker = Worker(
            client,
            task_queue=config.TEMPORAL_TASK_QUEUE,
            workflows=[OllamaWorkflow],
            activities=[get_ollama_response],
        )
        
        logger.info("Worker created successfully")
        logger.info("Starting worker...")
        
        # Add a timeout and better error handling
        try:
            logger.info("Worker is now running and waiting for tasks...")
            await worker.run()
        except asyncio.TimeoutError:
            logger.error("Worker startup timed out")
            raise
        except Exception as worker_error:
            logger.error(f"Worker runtime error: {worker_error}")
            raise
        
    except Exception as e:
        logger.error(f"Error starting worker: {e}")
        logger.error("This could be due to:")
        logger.error("1. Workflow definition issues")
        logger.error("2. Missing dependencies")
        logger.error("3. Temporal server connection problems")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker gracefully shut down.")