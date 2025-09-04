import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Centralized configuration class. Reads values from environment variables.
    """

    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
    AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
    AZURE_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
    AZURE_CHAT_DEPLOYMENT = os.getenv("AZURE_CHAT_DEPLOYMENT")

    # Databricks
    DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
    DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
    DATABRICKS_JOB_ID = os.getenv("DATABRICKS_JOB_ID")

    MAX_TOKENS=os.getenv("MAX_TOKENS")
    TEMPERATURE=os.getenv("TEMPERATURE")

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
