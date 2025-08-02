#!/usr/bin/env python3
"""
Configure Streamlit for ngrok access
This script reads your .env file and configures Streamlit to work with your ngrok domain
"""
import os
from dotenv import load_dotenv

def configure_streamlit_for_ngrok():
    # Load environment variables - check both current and parent directory
    parent_env = '../.env'
    local_env = '.env'
    
    if os.path.exists(parent_env):
        load_dotenv(parent_env)
        print(f"📁 Loading environment from: {parent_env}")
    elif os.path.exists(local_env):
        load_dotenv(local_env)
        print(f"📁 Loading environment from: {local_env}")
    else:
        print("❌ No .env file found in current directory or parent directory")
        return False
    
    ngrok_domain = os.getenv('NGROK_DOMAIN')
    
    if not ngrok_domain:
        print("❌ NGROK_DOMAIN not found in .env file")
        print("Please set NGROK_DOMAIN in your .env file first")
        return False
    
    # Create .streamlit directory if it doesn't exist
    streamlit_dir = '.streamlit'
    if not os.path.exists(streamlit_dir):
        os.makedirs(streamlit_dir)
    
    # Create config.toml
    config_content = f'''[server]
# Enable CORS protection (recommended for security)
enableCORS = true

# Enable XSRF protection (recommended for security)  
enableXsrfProtection = true

# Allow ngrok domain in CORS origins
corsAllowedOrigins = ["https://{ngrok_domain}"]

# Port configuration
port = 8501

[browser]
# Set the server address to your ngrok domain
serverAddress = "{ngrok_domain}"

# Use port 443 for HTTPS ngrok tunnels
serverPort = 443
'''

    config_path = os.path.join(streamlit_dir, 'config.toml')
    
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    print(f"✅ Streamlit configured for ngrok domain: {ngrok_domain}")
    print(f"   Config file created: {config_path}")
    print("\n🚀 Now you can:")
    print("   1. Start Streamlit: streamlit run app.py")
    print(f"   2. Expose via ngrok: make expose PORT=8501")
    print(f"   3. Access at: https://{ngrok_domain}")
    
    return True

if __name__ == "__main__":
    configure_streamlit_for_ngrok()
