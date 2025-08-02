#!/usr/bin/env python3
"""
Simple Temporal connection test
"""
import asyncio
import os
import sys
from temporalio.client import Client
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_local_path = os.path.join(parent_dir, '.env.local')
env_path = os.path.join(parent_dir, '.env')

if os.path.exists(env_local_path):
    load_dotenv(env_local_path)
elif os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

async def test_connection():
    temporal_host = os.getenv("TEMPORAL_HOST", "localhost")
    temporal_port = os.getenv("TEMPORAL_PORT", "7233")
    
    # Test different connection strings
    test_urls = [
        f"localhost:{temporal_port}",
        f"127.0.0.1:{temporal_port}",
        f"{temporal_host}:{temporal_port}",
    ]
    
    print(f"Environment variables:")
    print(f"  TEMPORAL_HOST: {temporal_host}")
    print(f"  TEMPORAL_PORT: {temporal_port}")
    print()
    
    for url in test_urls:
        try:
            print(f"Testing connection to: {url}")
            client = await Client.connect(url)
            print(f"✅ SUCCESS: Connected to {url}")
            
            # Test getting cluster info
            import temporalio.api.workflowservice.v1 as ws
            cluster_info = await client.workflow_service.get_cluster_info(
                ws.GetClusterInfoRequest()
            )
            print(f"   Cluster name: {cluster_info.cluster_name}")
            return client
            
        except Exception as e:
            print(f"❌ FAILED: {url} - {type(e).__name__}: {e}")
            print()
    
    print("All connection attempts failed!")
    return None

if __name__ == "__main__":
    asyncio.run(test_connection())
