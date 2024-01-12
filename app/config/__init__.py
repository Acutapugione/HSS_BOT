from .. enums import Settings
from os import getenv


class Config:
    TOKEN:str = getenv(Settings.TOKEN)
    API_HOST:str = getenv(Settings.API_HOST)
    API_PORT:str = getenv(Settings.API_PORT)