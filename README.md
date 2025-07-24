# Remote Ollama with ngrok

This project provides a simple and robust configuration to expose your local Ollama server to the internet using the `ngrok` agent. It uses a `Makefile` and a traffic policy file to ensure a stable and correctly configured tunnel.

This setup is based on the best practices found in the official `ngrok` documentation and community guides.

## Prerequisites

*   A local installation of [Ollama](https://ollama.com/).
*   An [ngrok account](https://dashboard.ngrok.com/signup) (a free account is sufficient).
*   The `ngrok` agent installed on your system. You can find installation instructions [here](https://ngrok.com/docs/getting-started/#2-install-the-ngrok-agent-cli).
*   `make` (usually pre-installed on macOS and Linux).

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/LaansDole/ngrok-ollama.git
    cd remote-ollama
    ```

2.  **Configure your ngrok Authtoken:**
    You must authenticate the `ngrok` agent. Get your authtoken from the [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken) and run the following command in your terminal, replacing `YOUR_NGROK_TOKEN` with your actual token:
    ```bash
    make setup # To see the documentation for setting up ngrok
    ngrok config add-authtoken YOUR_NGROK_TOKEN
    ```

3.  **Reserve a Domain:**
    This setup uses a static domain for a consistent URL. Reserve a free static domain on the [ngrok domains page](https://dashboard.ngrok.com/domains).

4.  **Configure Environment Variables:**
    *   Copy the example environment file: `cp .env.example .env`
    *   Edit the `.env` file and replace `YOUR_RESERVED_DOMAIN.ngrok.app` with the domain you reserved in the previous step.

5.  **Run the server:**
    ```bash
    make run
    ```

## Usage

1.  **Start your Ollama Server:**
    For `ngrok` to access your Ollama instance, you must start it so that it listens on all network interfaces. Open a new terminal and run:
    ```bash
    OLLAMA_HOST=0.0.0.0 ollama serve
    ```

2.  **Start the ngrok Tunnel:**
    In the project directory, simply run:
    ```bash
    make run
    ```
    This command will read your `.env` file and start the `ngrok` tunnel using the traffic policy defined in `ollama.yaml`. You will see the public URL in your terminal.

## Troubleshooting

Here are some common errors and their solutions:

### `ERR_NGROK_4018`: Authentication Failed

*   **Error Message:** `ERROR: authentication failed: Usage of ngrok requires a verified account and authtoken.`
*   **Solution:** This means your `ngrok` agent is not authenticated. Follow step 2 in the **Setup** section to add your authtoken.

### `Error reading configuration file 'ollama.yaml'`

*   **Error Messages:** `version property is required` or `field traffic_policy not found in type config.v2yamlConfig`
*   **Solution:** This indicates an issue with the traffic policy file or how it's being loaded. This project is pre-configured to handle this correctly, but ensure that the `run` command in the `Makefile` uses the `--traffic-policy-file` flag, not `--config`.

### Ollama Server Not Accessible from Tunnel

*   **Symptom:** The `ngrok` tunnel is running, but you get errors when trying to access your Ollama server through the public URL.
*   **Solution:** Ensure you have started the Ollama server as described in step 1 of the **Usage** section, with the `OLLAMA_HOST` environment variable set to `0.0.0.0`.

## Alternative Setup Methods

### Using Homebrew for Ollama (macOS)

If you are on macOS, you can install and manage Ollama as a system service using [Homebrew](https://brew.sh/).

1.  **Install Ollama:**
    ```bash
    brew install ollama
    ```

2.  **Start/Restart the Ollama Service:**
    This command will start the Ollama service in the background and ensure it restarts on login.
    ```bash
    brew services restart ollama
    ```
    With this setup, you may need to configure the `OLLAMA_HOST` environment variable for the service itself if you want it to be accessible from the ngrok tunnel.

### Using `pyngrok`

For those who prefer a Python-based approach, you can use the `pyngrok` library to manage the tunnel programmatically.

1.  **Installation**
    Install the required Python library:
    ```bash
    pip install pyngrok
    ```

2.  **Create the Script**
    Create a Python file (e.g., `expose_ollama.py`) with the following content:

    ```python
    import os
    import logging
    from pyngrok import ngrok

    # The default port for Ollama
    OLLAMA_PORT = 11434

    def setup_logging():
        """Sets up logging based on the LOG_LEVEL environment variable."""
        log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
        logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

    def expose_ollama():
        """
        Exposes the local Ollama server to the public using pyngrok.
        """
        setup_logging()

        try:
            # Check if OLLAMA_HOST is set correctly
            ollama_host = os.environ.get("OLLAMA_HOST", "").lower()
            if ollama_host not in ["0.0.0.0", "::"]:
                logging.warning("OLLAMA_HOST environment variable is not set to '0.0.0.0' or '::'.")
                logging.warning("The Ollama server may not be accessible from the ngrok tunnel.")
                logging.warning("Start Ollama with 'OLLAMA_HOST=0.0.0.0 ollama serve' for remote access.")

            # Get the ngrok authtoken from the environment variable
            auth_token = os.environ.get("NGROK_AUTHTOKEN")
            if auth_token:
                ngrok.set_auth_token(auth_token)
            else:
                logging.error("NGROK_AUTHTOKEN environment variable not set.")
                logging.error("Please set it to your ngrok authtoken.")
                logging.error("You can get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken")
                return

            # Open a HTTP tunnel to the Ollama port
            public_url = ngrok.connect(OLLAMA_PORT, "http")
            logging.info(f"Ollama is now exposed to the public at: {public_url}")
            logging.info("Press Ctrl+C to quit.")

            ngrok_process = ngrok.get_ngrok_process()
            try:
                # Block until CTRL-C or some other terminating event
                ngrok_process.proc.wait()
            except KeyboardInterrupt:
                logging.info("Shutting down ngrok tunnel.")
                ngrok.kill()

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            # Ensure ngrok processes are killed on error
            ngrok.kill()

    if __name__ == "__main__":
        expose_ollama()
    ```

3.  **Configuration and Usage**
    *   **Set Environment Variables:** This script requires the `NGROK_AUTHTOKEN` to be set as an environment variable.
        ```bash
        export NGROK_AUTHTOKEN="YOUR_NGROK_AUTHTOKEN"
        ```
    *   **Run the script:**
        ```bash
        python expose_ollama.py
        ```

## References

This project was built using information from the following resources:

*   **ngrok Documentation:** [Expose and Secure Your Self-Hosted Ollama API](https://ngrok.com/docs/universal-gateway/examples/ollama/)
*   **thoughtbot Blog:** [How to use ngrok and Ollama to access a local LLM remotely](https://thoughtbot.com/blog/ngrok-and-ollama)
*   **Ollama on Homebrew:** [formulae.brew.sh/formula/ollama](https://formulae.brew.sh/formula/ollama)