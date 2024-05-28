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
"""Example service."""

from enum import Enum
from typing import List
from pydantic import BaseModel

from my_project.config import settings
from my_project.models import Example


class ExceptionSource(str, Enum):
    """Exception source enum."""

    add_url = "add_url"
    diarization = "diarization"
    get_url = "get_url"
    post_processing = "post_processing"
    remove_url = "remove_url"
    transcription = "transcription"


class ProcessException(BaseModel):
    """Process exception model."""

    source: ExceptionSource
    message: str


class ExampleService:
    """Example Service."""

    def __init__(self) -> None:
        """Initialize ExampleService."""
        pass

    async def inference_warmup(self) -> None:
        """Warmup the GPU."""
        pass

    async def process_input(self) -> None:
        """Process input."""
        pass

    def example_function(self) -> List[str]:
        """Example function."""
        pass
