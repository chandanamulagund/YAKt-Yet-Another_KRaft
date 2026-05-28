import os

BROKER_HOST = os.getenv("BROKER_HOST", "127.0.0.1")
SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = os.getenv("SERVER_PORT", "5000")
BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"