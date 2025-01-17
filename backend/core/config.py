from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from typing import ClassVar
import os
import logging

# Logging setup
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Define absolute paths for .env files
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))  # Root directory (project-yoked/)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))  # Backend directory (project-yoked/backend/)

MAIN_ENV_PATH = os.path.join(ROOT_DIR, ".env")  # project-yoked/.env
BACKEND_ENV_PATH = os.path.join(BACKEND_DIR, ".env")  # project-yoked/backend/.env

# Load .env files
logger.debug(f"Loading main .env from: {MAIN_ENV_PATH}")
load_dotenv(MAIN_ENV_PATH)

logger.debug(f"Loading backend .env from: {BACKEND_ENV_PATH}")
load_dotenv(BACKEND_ENV_PATH)


class Settings(BaseSettings):
    # General settings
    APP_NAME: str = os.getenv("APP_NAME", "DefaultAppName")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.0.1")
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALLOWED_HOSTS: str = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/default_db")

    # Stripe API keys
    STRIPE_PUBLIC_KEY: str = os.getenv("STRIPE_PUBLIC_KEY", "your_stripe_public_key")
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "your_stripe_secret_key")

    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")

    # Email settings for FastAPI-Mail
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "default_email@example.com")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "default_password")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "default_email@example.com")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 587))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS", "True").lower() == "true"
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS", "False").lower() == "true"
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS", "True").lower() == "true"

    #AWS
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "your_access_key_id")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "your_secret_access_key")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "your_s3_bucket_name")

    #Vimeo
    VIMEO_CLIENT_ID: str = os.getenv("VIMEO_CLIENT_ID", "your_client_id")
    VIMEO_CLIENT_SECRET: str = os.getenv("VIMEO_CLIENT_SECRET", "your_client_secret")
    VIMEO_ACCESS_TOKEN: str = os.getenv("VIMEO_ACCESS_TOKEN", "your_access_token")

    # Third-party API keys
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "your_google_maps_api_key")
    PUSH_NOTIFICATIONS_API_KEY: str = os.getenv("PUSH_NOTIFICATIONS_API_KEY", "your_push_notifications_api_key")

    # OAuth2 settings
    oauth2_scheme: ClassVar[OAuth2PasswordBearer] = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    class Config:
        env_file = BACKEND_ENV_PATH


settings = Settings()

# Log loaded settings for debugging
logger.debug(f"Settings loaded: {settings.dict()}")
