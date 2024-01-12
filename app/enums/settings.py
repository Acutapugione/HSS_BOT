from enum import Enum


class Settings(str, Enum):
    TOKEN:str = "TOKEN"
    API_HOST: str = "API_HOST"
    API_PORT: str = "API_PORT"