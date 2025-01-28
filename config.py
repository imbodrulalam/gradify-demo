import os
from dotenv import load_dotenv
load_dotenv()  # This will load environment variables from your .env file


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing-specific configuration."""
    TESTING = True
    DEBUG = True
