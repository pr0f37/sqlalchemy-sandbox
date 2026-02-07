import os
from pathlib import Path
from typing import Self
from sqlalchemy_sandbox.utils.read_yaml import read_yaml_file, find_file
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel, Field, TypeAdapter
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class DBConfig(BaseModel):
    host: str = Field(default="localhost")
    port: int = Field(default=5432, gt=0, lt=9999)
    db: str = Field(default="local")
    user: str = Field(default="postgres")
    password: str = Field(default="postgres")


db_config_type = TypeAdapter(dict[str, DBConfig])


class Config(BaseSettings):
    """My config class"""

    DB_FILE_NAME: str = Field(default="db_config.yaml")
    DATABASES: dict[str, DBConfig] = Field(default_factory=dict)

    def _parse_db_config_file(self):
        current_dir = Path(os.path.dirname(os.path.realpath(__file__)))
        try:
            db_file = find_file(current_dir, self.DB_FILE_NAME)
            db_config = read_yaml_file(db_file)
        except FileNotFoundError as ex:
            db_config = {"default": DBConfig()}
            print("DB config not found - failover to default")
            print(str(ex))
        self.DATABASES = db_config_type.validate_python(db_config)

    @classmethod
    def get_config(cls) -> Self:
        config = cls()
        config._parse_db_config_file()
        return config


app_config = Config.get_config()
