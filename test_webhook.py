import os
from dotenv import load_dotenv

# Load .env file from the current directory explicitly, overriding system variables
load_dotenv(".env", override=True)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
print(f"Webhook URL: {WEBHOOK_URL}")

# Also print the current working directory to verify we're in the right place
print(f"Current directory: {os.getcwd()}")