.PHONY: setup run

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