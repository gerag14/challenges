from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    # DB
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./db/test.sqlite"

    # SMTP
    SMTP_TLS: bool = True
    SMTP_PORT: int
    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PASSWORD: str

    # EMAIL
    EMAILS_FROM_EMAIL: EmailStr = None
    EMAILS_FROM_NAME: str
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"

    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str = "us-east-1"
    AWS_BUCKET: str = "transactions"


settings = Settings()  # noqa
