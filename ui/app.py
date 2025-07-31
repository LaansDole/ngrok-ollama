import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from temporalio.client import Client
from temporal_workflow import OllamaWorkflow

# Load environment variables from .env file
load_dotenv()

# --- Constants ---
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama2")
TEMPORAL_TASK_QUEUE = os.getenv("TEMPORAL_TASK_QUEUE", "ollama-task-queue")
TEMPORAL_HOST = os.getenv("TEMPORAL_HOST", "localhost")

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Ollama Chat",
    page_icon="🤖",
    layout="wide",
)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Temporal Client Helper ---
async def get_temporal_response(model: str, messages: list) -> str:
    """Connects to Temporal and runs the Ollama workflow."""
    try:
        client = await Client.connect(f"{TEMPORAL_HOST}:7233")
        result = await client.execute_workflow(
            OllamaWorkflow.run,
            args=[model, messages],
            id="ollama-workflow",
            task_queue=TEMPORAL_TASK_QUEUE,
        )
        return result
    except Exception as e:
        return f"Error communicating with Temporal: {e}"

# --- UI Components ---
st.title("Ollama Chat (with Temporal)")
st.caption("A Streamlit UI for Ollama, with Temporal for request handling.")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Main Chat Logic ---
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Get the current event loop
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:  # 'RuntimeError: There is no current event loop...'
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Run the Temporal workflow in the event loop
            response = loop.run_until_complete(get_temporal_response(DEFAULT_MODEL, st.session_state.messages))
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})