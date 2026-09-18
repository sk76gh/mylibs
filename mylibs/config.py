import os

# 1. (Optional) If you also develop locally outside of Codespaces with a .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # If python-dotenv isn't installed, skip it (Codespaces doesn't need it)


class Config:
    """Centralized application configuration and secrets."""
    
    # API Keys
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    HF_API_KEY = os.environ.get("HUGGINGFACEHUB_API_TOKEN")  # Hugging Face API Key
    OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY")
    # Database Settings
    DB_URL = os.environ.get("DATABASE_URL", "sqlite:///default.db") # Keeps a default fallback
    
    # App Settings
    #ENVIRONMENT = os.environ.get("APP_ENV", "development")
    #PORT = int(os.environ.get("PORT", 8080))
    LogLevel=os.environ.get("LOG_LEVEL", "INFO")  # Default to INFO if not set

    @classmethod
    def validate(cls):
        print(cls.__dict__)
        """Optional: Ensures critical secrets are not missing before the app starts."""
        missing = [key for key in ["GEMINI_API_KEY"] if not getattr(cls, key)]
        print(f"Missing---: {missing}")
        if missing:
            raise ValueError(f"❌ Missing critical environment secrets: {', '.join(missing)}")

# Validate secrets as soon as this file is imported anywhere in your project
#Config.validate()  # Uncomment this line to enforce validation on import
