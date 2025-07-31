.PHONY: setup run test-latency help ui-install ui-run ui-worker

help:
	@echo "Available commands:"
	@echo "  setup        - Display ngrok setup instructions"
	@echo "  run          - Start the ngrok tunnel for Ollama"
	@echo "  test-latency - Test latency performance of the tunnel"
	@echo "  ui-install   - Install UI dependencies"
	@echo "  ui-run       - Run the Streamlit UI"
	@echo "  ui-worker    - Run the Temporal worker"
	@echo "  help         - Show this help message"

setup:
	@echo "Please follow these steps to configure ngrok:"
	@echo "1. If you don't have an ngrok account, sign up at https://dashboard.ngrok.com/signup"
	@echo "2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken"
	@echo "3. Run the following command to add your authtoken to the ngrok agent:"
	@echo "   ngrok config add-authtoken YOUR_AUTHTOKEN"
	@echo "4. Reserve a static domain at https://dashboard.ngrok.com/domains"
	@echo "5. Update the NGROK_DOMAIN in your .env file with your reserved domain."

run:
	@echo "Starting the Ollama ngrok tunnel..."
	@source .env && ngrok http 11434 --domain $$NGROK_DOMAIN --traffic-policy-file ollama.yaml

test-latency:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Please configure your ngrok domain first."; \
		exit 1; \
	fi
	@source .env && ./scripts/test-latency.sh https://$$NGROK_DOMAIN

ui-install:
	@echo "Installing UI dependencies..."
	@pip install -r ui/requirements.txt

ui-run:
	@echo "Running the Streamlit UI..."
	@streamlit run ui/app.py

ui-worker:
	@echo "Running the Temporal worker in another terminal..."
	@python ui/worker.py
