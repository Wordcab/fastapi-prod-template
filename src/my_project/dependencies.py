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
"""Dependencies module."""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from my_project.config import settings
from my_project.utils import retrieve_user_platform
from my_project.services.example_service import ExampleService

# Define the maximum number of files to pre-download
download_limit = asyncio.Semaphore(10)

# Define the ASR service to use depending on the settings
service = ExampleService()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Context manager to handle the startup and shutdown of the application."""
    if retrieve_user_platform() != "linux":
        logger.warning(
            "You are not running the application on Linux.\nThe application was tested"
            " on Ubuntu 22.04, so we cannot guarantee that it will work on other"
            " OS.\nReport any issues with your env specs to:"
            " https://github.com/Wordcab/wordcab-transcribe/issues"
        )

    logger.info("Warmup initialization...")
    await service.inference_warmup()

    yield  # This is where the execution of the application starts
