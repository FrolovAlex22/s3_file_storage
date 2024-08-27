import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

from crud.s3_client import S3Client


load_dotenv()

ACCESS_KEY=os.environ.get("S3_ACCESS_KEY")
SECRET_KEY=os.environ.get("S3_SECRET_KEY")
BUCKET_NAME=os.environ.get("S3_BUCKET_NAME")
DB_HOST=os.environ.get("DB_HOST")
DB_PORT=os.environ.get("DB_PORT")
DB_USER=os.environ.get("DB_USER")
DB_PASS=os.environ.get("DB_PASS")
DB_NAME=os.environ.get("DB_NAME")

DOCKER = os.environ.get("DOCKER", "True") == "True"

s3_client = S3Client(
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    endpoint_url="https://s3.storage.selcloud.ru",  # для Selectel используйте https://s3.storage.selcloud.ru
    bucket_name=BUCKET_NAME)


class AppSettings(BaseSettings):
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    app_title: str = "S3_file_storage"
    project_name: str = "API S3_file_storage"
    project_host: str = "0.0.0.0"
    project_port: int = 8000


settings = AppSettings()

# class Settings(BaseSettings):
#     # DATABASE_URL: str = (
#     #     f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#     # )
#     app_title: str = "sending_messages"
#     project_name: str = "API Sending_messages"
#     project_host: str = "0.0.0.0"
#     project_port: int = 8006
#     mailcow_x_api_key: str
#     mailcow_5d_hub_url: str


# settings = Settings()

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
