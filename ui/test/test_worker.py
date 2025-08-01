#!/usr/bin/env python3
"""
Test script to verify Temporal worker setup
"""
import asyncio
import signal
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from temporalio.worker import Worker
from temporal_workflow import OllamaWorkflow, get_ollama_response
from temporal_manager import temporal_manager
from temporal_config import config
from logger import logger

class WorkerTester:
    def __init__(self):
        self.worker = None
        self.client = None
        
    async def test_connection(self):
        """Test if we can connect to Temporal"""
        try:
            self.client = await temporal_manager.get_client()
            if not self.client:
                logger.error("Failed to connect to Temporal")
                return False
                
            # Try to get cluster info
            import temporalio.client
            import temporalio.api.workflowservice.v1 as ws
            cluster_info = await self.client.workflow_service.get_cluster_info(
                ws.GetClusterInfoRequest()
            )
            logger.info(f"Connected to Temporal cluster: {cluster_info.cluster_name}")
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    async def create_worker(self):
        """Create the worker"""
        try:
            self.worker = Worker(
                self.client,
                task_queue=config.TEMPORAL_TASK_QUEUE,
                workflows=[OllamaWorkflow],
                activities=[get_ollama_response],
            )
            logger.info("Worker created successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to create worker: {e}")
            return False
    
    async def run_worker_with_timeout(self, timeout_seconds=10):
        """Run worker with a timeout to test if it starts properly"""
        try:
            logger.info(f"Starting worker for {timeout_seconds} seconds...")
            await asyncio.wait_for(self.worker.run(), timeout=timeout_seconds)
        except asyncio.TimeoutError:
            logger.info("Worker ran successfully for the timeout period")
            return True
        except Exception as e:
            logger.error(f"Worker failed: {e}")
            return False

async def main():
    tester = WorkerTester()
    
    # Test connection
    logger.info("=== Testing Temporal Connection ===")
    if not await tester.test_connection():
        return
    
    # Create worker
    logger.info("=== Creating Worker ===")
    if not await tester.create_worker():
        return
    
    # Test worker startup
    logger.info("=== Testing Worker Startup ===")
    success = await tester.run_worker_with_timeout(5)
    
    if success:
        logger.info("✅ Worker test completed successfully!")
        logger.info("The worker appears to be working correctly.")
        logger.info("If the original worker seems 'stuck', it's actually running normally and waiting for tasks.")
    else:
        logger.error("❌ Worker test failed!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        logger.error(f"Test failed with exception: {e}")
