# System Design: Streamlit-based Ollama Client UI with Temporal

This document outlines the final implementation of a web-based client UI for the Ollama server, built with Streamlit and integrated with Temporal for robust request handling.

## 1. High-Level Architecture

The architecture consists of the following components:

1.  **Streamlit Application:** A Python script that serves as the user interface, managing the chat window, message display, and user input.
2.  **Temporal Workflow:** A Temporal workflow and activity that offloads Ollama API requests from the main UI thread, allowing for non-blocking, concurrent request management.
3.  **Temporal Worker:** A separate Python process that executes the workflow and activity.
4.  **API Gateway (`ngrok`):** The `ngrok` tunnel exposes the Streamlit application to the internet.
5.  **Backend (Ollama):** The local Ollama server handles the AI inference requests.

## 2. Technology Stack

*   **UI Framework:** Streamlit
*   **Task Queue:** Temporal
*   **Language:** Python
*   **API Communication:** `requests` library

## 3. Project Structure

The `ui` directory houses the application:

```
/
├── ui/
│   ├── app.py              # The main Streamlit application
│   ├── temporal_workflow.py # The Temporal workflow and activity
│   ├── worker.py           # The Temporal worker
│   └── requirements.txt      # Python dependencies
└── ... (existing project files)
```

## 4. Implementation Details

1.  **Streamlit Application (`app.py`):**
    *   The UI is built with Streamlit components, including `st.chat_message` and `st.chat_input`.
    *   When a user submits a prompt, the application calls a Temporal workflow to get the response from the Ollama API.
    *   The UI uses `st.spinner` to indicate that the request is being processed.

2.  **Temporal Workflow (`temporal_workflow.py`):**
    *   An `OllamaWorkflow` is defined to manage the process of getting a response from the Ollama API.
    *   A `get_ollama_response` activity contains the logic for making the `requests.post` call to the Ollama API.

3.  **Temporal Worker (`worker.py`):**
    *   The worker connects to the Temporal server and listens on the `ollama-task-queue` for tasks.
    *   It executes the `get_ollama_response` activity when a workflow is initiated.

4.  **Makefile:**
    *   The `Makefile` has been updated with the following commands:
        *   `ui-install`: Installs the Python dependencies from `ui/requirements.txt`.
        *   `ui-run`: Starts the Streamlit application.
        *   `ui-worker`: Starts the Temporal worker.

## 5. Concurrency

By integrating Temporal, the application can handle concurrent requests efficiently. Each chat session in Streamlit can trigger a separate Temporal workflow, which are then processed by the worker. This prevents the UI from blocking and ensures a smooth user experience, even with multiple users.
