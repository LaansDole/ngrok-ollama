import asyncio
import os
from typing import Optional
from temporalio.client import Client
from dotenv import load_dotenv
from logger import logger

# Load environment variables from .env file
# Check for local environment file first
if os.path.exists('.env.local'):
    load_dotenv('.env.local')
else:
    load_dotenv()

class TemporalManager:
    def __init__(self):
        self.client: Optional[Client] = None
        self.temporal_host = os.getenv("TEMPORAL_HOST", "localhost")
        self.temporal_port = os.getenv("TEMPORAL_PORT", "7233")
        
    async def get_client(self) -> Optional[Client]:
        """Get Temporal client with connection retry logic."""
        if self.client:
            return self.client
            
        # For local development, prioritize localhost connections
        # Check if we're likely running in Docker vs locally
        is_docker = os.path.exists('/.dockerenv') or os.getenv('DOCKER_ENVIRONMENT') == 'true'
        
        if is_docker:
            # Docker environment - try Docker service names first
            connection_attempts = [
                f"{self.temporal_host}:{self.temporal_port}",
                f"temporal:{self.temporal_port}",
                f"localhost:{self.temporal_port}",
                f"127.0.0.1:{self.temporal_port}",
            ]
        else:
            # Local development - prioritize localhost
            connection_attempts = [
                f"localhost:{self.temporal_port}",
                f"127.0.0.1:{self.temporal_port}",
                f"{self.temporal_host}:{self.temporal_port}",
                f"temporal:{self.temporal_port}",
            ]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_attempts = []
        for attempt in connection_attempts:
            if attempt not in seen:
                seen.add(attempt)
                unique_attempts.append(attempt)
        
        for attempt_url in unique_attempts:
            try:
                logger.info(f"Attempting to connect to Temporal at: {attempt_url}")
                self.client = await Client.connect(attempt_url)
                logger.info(f"Successfully connected to Temporal at: {attempt_url}")
                return self.client
            except Exception as e:
                logger.warning(f"Failed to connect to {attempt_url}: {e}")
                continue
                
        logger.error("Failed to connect to Temporal server. Please ensure:")
        logger.error("1. Temporal server is running")
        logger.error("2. Check your TEMPORAL_HOST environment variable")
        logger.error("3. Verify network connectivity")
        logger.error("4. If using Docker, ensure services are in the same network")
        return None

# Global temporal manager instance
temporal_manager = TemporalManager()
