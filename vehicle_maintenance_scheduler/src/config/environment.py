import os
from dotenv import load_dotenv

load_dotenv()

class Environment:
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    
    # Candidate Info
    EMAIL = os.getenv("EMAIL", "")
    NAME = os.getenv("NAME", "")
    ROLL_NO = os.getenv("ROLL_NO", "")
    ACCESS_CODE = os.getenv("ACCESS_CODE", "")
    GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "")
    
    # Secrets
    CLIENT_ID = os.getenv("CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")

env = Environment()
