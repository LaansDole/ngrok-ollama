#!/usr/bin/env python3
"""
Test the Streamlit app's Temporal connection function
"""
import asyncio
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from temporal_manager import temporal_manager

async def test_streamlit_connection():
    """Test the same connection method used by Streamlit"""
    print("Testing Streamlit's Temporal connection method...")
    
    try:
        client = await temporal_manager.get_client()
        if not client:
            print("❌ Failed to get client")
            return False
            
        print("✅ Successfully got Temporal client")
        
        # Test a simple operation
        import temporalio.api.workflowservice.v1 as ws
        cluster_info = await client.workflow_service.get_cluster_info(
            ws.GetClusterInfoRequest()
        )
        print(f"✅ Cluster info retrieved: {cluster_info.cluster_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_streamlit_connection())
    if success:
        print("\n🎉 Streamlit connection should work now!")
    else:
        print("\n💥 There's still an issue with the connection.")
