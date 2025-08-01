# UI Tests

This directory contains test scripts for the remote-ollama UI components.

## Test Files

- **`test_connection.py`** - Tests basic Temporal server connection with different URLs
- **`test_streamlit_connection.py`** - Tests the Streamlit app's Temporal connection method
- **`test_worker.py`** - Tests Temporal worker creation and startup functionality

## Running Tests

### Run Individual Tests

```bash
# From the ui directory
python3 test/test_connection.py
python3 test/test_streamlit_connection.py  
python3 test/test_worker.py
```

### Run All Tests

```bash
# From the ui directory
python3 test/run_all_tests.py
```

## Prerequisites

Make sure you have:
1. Temporal server running (usually on localhost:7233)
2. Required Python packages installed (`pip install -r requirements.txt`)
3. Environment variables configured (`.env.local` or `.env` file)

## Test Descriptions

### test_connection.py
- Tests basic connectivity to Temporal server
- Tries multiple connection URLs (localhost, 127.0.0.1, etc.)
- Verifies cluster information retrieval

### test_streamlit_connection.py  
- Tests the same connection method used by the Streamlit app
- Uses the `temporal_manager` for connection handling
- Verifies the connection works with proper retry logic

### test_worker.py
- Tests worker creation and registration with Temporal
- Verifies worker can start and run for a timeout period
- Tests workflow and activity registration

## Troubleshooting

If tests fail:
1. Ensure Temporal server is running: `lsof -i :7233`
2. Check environment variables in `.env.local`
3. Verify all Python dependencies are installed
4. Check network connectivity to Temporal server
