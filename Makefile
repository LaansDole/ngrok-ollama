.PHONY: setup expose test-latency help ui-install ui-run ui-worker run-worker run-temporal stop-temporal ui-compose debug-worker run-worker-local configure-streamlit

help:
	@echo "Available commands:"
	@echo "  setup        - Display ngrok setup instructions"
	@echo "  expose       - Start the ngrok tunnel (default port 8501)"
	@echo "                 Usage: make expose [PORT=<port>]"
	@echo "  test-latency - Test latency performance of the tunnel"
	@echo "  ui-install   - Install UI dependencies"
	@echo "  ui-run       - Run the Streamlit UI"
	@echo "  ui-worker    - Run the Temporal worker"
	@echo "  run-temporal - Start Temporal server with docker-compose"
	@echo "  stop-temporal - Stop Temporal server docker-compose services"
	@echo "  configure-streamlit - Configure Streamlit for ngrok access"
	@echo "  debug-worker - Run the worker with debug output"
	@echo "  run-worker-local - Run worker optimized for local development"
	@echo "  help         - Show this help message"

setup:
	@echo "Please follow these steps to configure ngrok:"
	@echo "1. If you don't have an ngrok account, sign up at https://dashboard.ngrok.com/signup"
	@echo "2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken"
	@echo "3. Run the following command to add your authtoken to the ngrok agent:"
	@echo "   ngrok config add-authtoken YOUR_AUTHTOKEN"
	@echo "4. Reserve a static domain at https://dashboard.ngrok.com/domains"
	@echo "5. Update the NGROK_DOMAIN in your .env file with your reserved domain."

expose:
	@echo "Starting the Ollama ngrok tunnel..."
	@PORT=$${PORT:-8501}; \
	echo "Exposing port $$PORT"; \
	source .env && ngrok http $$PORT --domain $$NGROK_DOMAIN --traffic-policy-file ollama.yaml

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
	@cd ui && source venv/bin/activate && streamlit run app.py

ui-worker: run-temporal run-worker

run-worker:
	@echo "Running the Temporal worker in another terminal..."
	@cd ui && source venv/bin/activate && python3 worker.py

run-temporal:
	@echo "Starting Temporal server with docker-compose..."
	@if ! lsof -Pi :7233 -sTCP:LISTEN -t >/dev/null 2>&1; then \
		echo "Temporal server not running, starting it..."; \
		cd ui/docker-compose && docker-compose up -d; \
		echo "Temporal server started with docker-compose"; \
		echo "Waiting for services to be ready..."; \
		sleep 10; \
		echo "Temporal Web UI available at: http://localhost:8080"; \
	else \
		echo "Temporal server already running on port 7233"; \
	fi

stop-temporal:
	@echo "Stopping Temporal server docker-compose services..."
	@cd ui/docker-compose && docker-compose down
	@echo "Temporal server stopped"

configure-streamlit:
	@echo "Configuring Streamlit for ngrok access..."
	@cd ui && python3 configure_ngrok.py