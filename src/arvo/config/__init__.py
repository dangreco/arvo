import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from arvo.config.jwt import JwtConfig


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.test" if os.getenv("ENV") == "test" else ".env"),
        env_file_encoding="utf-8",
        cli_parse_args=True,
        env_nested_delimiter="__",
    )

    jwt: JwtConfig


config = Config()  # ty: ignore

__all__ = ["config"]
