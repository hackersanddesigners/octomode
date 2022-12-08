import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Bind them to Python variables
APPLICATION_ROOT = os.environ.get('OCTOMODE_APPLICATION_ROOT', '/')
PORTNUMBER = int(os.environ.get('OCTOMODE_PORTNUMBER', 5001))
PAD_URL = os.environ.get('OCTOMODE_PAD_URL', 'https://pad.vvvvvvaria.org')
PAD_API_URL = os.environ.get('OCTOMODE_PAD_API_URL', 'https://pad.vvvvvvaria.org/api/1.2.15')
PAD_API_KEY = os.environ.get('OCTOMODE_PAD_API_KEY', '')

# Check if API key is provided
if not PAD_API_KEY or PAD_API_KEY == "XXX":
    print("error: you must provide a value for OCTOMODE_PAD_API_KEY")
    print("error: e.g. export OCTOMODE_PAD_API_KEY=...")
    exit(1)