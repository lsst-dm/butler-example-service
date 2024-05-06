"""Configuration definition."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from safir.logging import LogLevel, Profile

__all__ = ["Config", "config"]


class Config(BaseSettings):
    """Configuration for butler-example-service."""

    name: str = Field("butler-example-service", title="Name of application")

    path_prefix: str = Field(
        "/butler-example-service", title="URL prefix for application"
    )

    profile: Profile = Field(
        Profile.development, title="Application logging profile"
    )

    log_level: LogLevel = Field(
        LogLevel.INFO, title="Log level of the application's logger"
    )

    model_config = SettingsConfigDict(
        env_prefix="BUTLER_EXAMPLE_SERVICE_", case_sensitive=False
    )


config = Config()
"""Configuration for butler-example-service."""
