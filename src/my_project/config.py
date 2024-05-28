# Copyright 2024 The Wordcab Team. All rights reserved.
#
# Licensed under the MIT License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://github.com/Wordcab/wordcab-transcribe/blob/main/LICENSE
#
# Except as expressly provided otherwise herein, and to the fullest
# extent permitted by law, Licensor provides the Software (and each
# Contributor provides its Contributions) AS IS, and Licensor
# disclaims all warranties or guarantees of any kind, express or
# implied, whether arising under any law or from any usage in trade,
# or otherwise including but not limited to the implied warranties
# of merchantability, non-infringement, quiet enjoyment, fitness
# for a particular purpose, or otherwise.
#
# See the License for the specific language governing permissions
# and limitations under the License.
"""Configuration module."""

from os import getenv

from dotenv import load_dotenv
from loguru import logger
from pydantic import field_validator
from pydantic.dataclasses import dataclass

from my_project import __version__


@dataclass
class Settings:
    """Configuration settings for the Wordcab Transcribe API."""

    # General configuration
    project_name: str
    version: str
    description: str
    api_prefix: str
    debug: bool
    # API authentication configuration
    username: str
    password: str
    openssl_key: str
    openssl_algorithm: str
    access_token_expire_minutes: int
    # AWS configuration
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_storage_bucket_name: str
    aws_region_name: str
    # Svix configuration
    svix_api_key: str
    svix_app_id: str

    @field_validator("project_name")
    def project_name_must_not_be_none(cls, value: str):  # noqa: B902, N805
        """Check that the project_name is not None."""
        if value is None:
            raise ValueError(
                "`project_name` must not be None, please verify the `.env` file."
            )

        return value

    @field_validator("version")
    def version_must_not_be_none(cls, value: str):  # noqa: B902, N805
        """Check that the version is not None."""
        if value is None:
            raise ValueError(
                "`version` must not be None, please verify the `.env` file."
            )

        return value

    @field_validator("description")
    def description_must_not_be_none(cls, value: str):  # noqa: B902, N805
        """Check that the description is not None."""
        if value is None:
            raise ValueError(
                "`description` must not be None, please verify the `.env` file."
            )

        return value

    @field_validator("api_prefix")
    def api_prefix_must_not_be_none(cls, value: str):  # noqa: B902, N805
        """Check that the api_prefix is not None."""
        if value is None:
            raise ValueError(
                "`api_prefix` must not be None, please verify the `.env` file."
            )

        return value

    @field_validator("openssl_algorithm")
    def openssl_algorithm_must_be_valid(cls, value: str):  # noqa: B902, N805
        """Check that the OpenSSL algorithm is valid."""
        if value not in {"HS256", "HS384", "HS512"}:
            raise ValueError(
                "openssl_algorithm must be a valid algorithm, please verify the `.env`"
                " file."
            )

        return value

    @field_validator("access_token_expire_minutes")
    def access_token_expire_minutes_must_be_valid(cls, value: int):  # noqa: B902, N805
        """Check that the access token expiration is valid. Only if debug is False."""
        if value <= 0:
            raise ValueError(
                "access_token_expire_minutes must be positive, please verify the `.env`"
                " file."
            )

        return value

    def __post_init__(self):
        """Post initialization checks."""
        if self.debug is False:
            if self.username == "admin" or self.username is None:  # noqa: S105
                logger.warning(
                    f"Username is set to `{self.username}`, which is not secure for"
                    " production."
                )
            if self.password == "admin" or self.password is None:  # noqa: S105
                logger.warning(
                    f"Password is set to `{self.password}`, which is not secure for"
                    " production."
                )
            if (
                self.openssl_key == "0123456789abcdefghijklmnopqrstuvwyz"  # noqa: S105
                or self.openssl_key is None
            ):
                logger.warning(
                    f"OpenSSL key is set to `{self.openssl_key}`, which is the default"
                    " encryption key. It's absolutely not secure for production."
                    " Please change it in the `.env` file. You can generate a new key"
                    " with `openssl rand -hex 32`."
                )


load_dotenv()

settings = Settings(
    # General configuration
    project_name=getenv("PROJECT_NAME", "My Project"),
    version=getenv("VERSION", __version__),
    description=getenv(
        "DESCRIPTION",
        "My project."
    ),
    api_prefix=getenv("API_PREFIX", "/api/v1"),
    debug=getenv("DEBUG", True),
    # API authentication configuration
    username=getenv("USERNAME", "admin"),
    password=getenv("PASSWORD", "admin"),
    openssl_key=getenv("OPENSSL_KEY", "0123456789abcdefghijklmnopqrstuvwyz"),  # Change in prod
    openssl_algorithm=getenv("OPENSSL_ALGORITHM", "HS256"),
    access_token_expire_minutes=getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30),
    # Svix configuration
    svix_api_key=getenv("SVIX_API_KEY", ""),
    svix_app_id=getenv("SVIX_APP_ID", ""),
)
