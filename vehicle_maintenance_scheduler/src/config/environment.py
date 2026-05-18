import os
from dotenv import load_dotenv

load_dotenv()

class Environment:
    @property
    def BASE_URL(self) -> str:
        load_dotenv(override=True)
        return os.getenv("BASE_URL", "http://localhost:8000")
    
    # Candidate Info
    @property
    def EMAIL(self) -> str:
        load_dotenv(override=True)
        return os.getenv("EMAIL", "")

    @property
    def NAME(self) -> str:
        load_dotenv(override=True)
        return os.getenv("NAME", "")

    @property
    def ROLL_NO(self) -> str:
        load_dotenv(override=True)
        return os.getenv("ROLL_NO", "")

    @property
    def ACCESS_CODE(self) -> str:
        load_dotenv(override=True)
        return os.getenv("ACCESS_CODE", "")

    @property
    def GITHUB_USERNAME(self) -> str:
        load_dotenv(override=True)
        return os.getenv("GITHUB_USERNAME", "")
    
    # Secrets
    @property
    def CLIENT_ID(self) -> str:
        load_dotenv(override=True)
        return os.getenv("CLIENT_ID", "")

    @property
    def CLIENT_SECRET(self) -> str:
        load_dotenv(override=True)
        return os.getenv("CLIENT_SECRET", "")

    @property
    def ACCESS_TOKEN(self) -> str:
        load_dotenv(override=True)
        return os.getenv("ACCESS_TOKEN", "")

env = Environment()
