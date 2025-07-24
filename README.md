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
    git clone <repository-url>
    cd remote-ollama
    ```

2.  **Configure your ngrok Authtoken:**
    You must authenticate the `ngrok` agent. Get your authtoken from the [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken) and run the following command in your terminal, replacing `YOUR_NGROK_TOKEN` with your actual token:
    ```bash
    ngrok config add-authtoken YOUR_NGROK_TOKEN
    ```

3.  **Reserve a Domain:**
    This setup uses a static domain for a consistent URL. Reserve a free static domain on the [ngrok domains page](https://dashboard.ngrok.com/domains).

4.  **Configure Environment Variables:**
    *   Copy the example environment file: `cp .env.example .env`
    *   Edit the `.env` file and replace `YOUR_RESERVED_DOMAIN.ngrok.app` with the domain you reserved in the previous step.

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

## References

This project was built using information from the following resources:

*   **ngrok Documentation:** [Expose and Secure Your Self-Hosted Ollama API](https://ngrok.com/docs/universal-gateway/examples/ollama/)
*   **thoughtbot Blog:** [How to use ngrok and Ollama to access a local LLM remotely](https://thoughtbot.com/blog/ngrok-and-ollama)
