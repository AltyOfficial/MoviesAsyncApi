import os
import pathlib

from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()


class Settings(BaseSettings):

    BASE_DIR = pathlib.Path(__file__).parent.parent

    SECRET_KEY = os.getenv('SECRET_KEY')

    # PostgreSQL
    USERNAME = os.getenv('POSTGRES_USER')
    PASSWORD = os.getenv('POSTGRES_PASSWORD')
    HOST = os.getenv('POSTGRES_HOST')
    PORT = os.getenv('POSTGRES_PORT')
    DATABASE_NAME = os.getenv('POSTGRES_DB')

    # Redis
    REDIS_HOST: str = os.getenv('REDIS_HOST')
    REDIS_PORT: str = os.getenv('REDIS_PORT')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
