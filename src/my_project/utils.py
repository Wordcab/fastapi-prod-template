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
"""Utils module."""
import re
import sys
import asyncio
import aiofiles
import subprocess  # noqa: S404
from pathlib import Path
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

import boto3
from my_project.config import settings

from loguru import logger
from svix.api import MessageIn, SvixAsync

if TYPE_CHECKING:
    from fastapi import UploadFile


# pragma: no cover
async def async_run_subprocess(command: List[str]) -> tuple:
    """
    Run a subprocess asynchronously.

    Args:
        command (List[str]): Command to run.

    Returns:
        tuple: Tuple with the return code, stdout and stderr.
    """
    process = await asyncio.create_subprocess_exec(
        *command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    return process.returncode, stdout, stderr


# pragma: no cover
def run_subprocess(command: List[str]) -> tuple:
    """
    Run a subprocess synchronously.

    Args:
        command (List[str]): Command to run.

    Returns:
        tuple: Tuple with the return code, stdout and stderr.
    """
    process = subprocess.Popen(  # noqa: S603,S607
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    return process.returncode, stdout, stderr


def delete_file(filepath: Union[str, Tuple[str, Optional[str]]]) -> None:
    """
    Delete a file or a list of files.

    Args:
        filepath (Union[str, Tuple[str]]): Path to the file to delete.
    """
    if isinstance(filepath, str):
        filepath = (filepath, None)

    for path in filepath:
        if path:
            Path(path).unlink(missing_ok=True)


def is_empty_string(text: str):
    """
    Checks if a string is empty after removing spaces and periods.

    Args:
        text (str): The text to check.

    Returns:
        bool: True if the string is empty, False otherwise.
    """
    text = text.replace(".", "")
    text = re.sub(r"\s+", "", text)
    if text.strip():
        return False
    return True


def format_punct(text: str):
    """
    Removes Whisper's '...' output, and checks for weird spacing in punctuation. Also removes extra spaces.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    text = text.strip()

    if text[0].islower():
        text = text[0].upper() + text[1:]
    if text[-1] not in [".", "?", "!", ":", ";", ","]:
        text += "."

    text = text.replace("...", "")
    text = text.replace(" ?", "?")
    text = text.replace(" !", "!")
    text = text.replace(" .", ".")
    text = text.replace(" ,", ",")
    text = text.replace(" :", ":")
    text = text.replace(" ;", ";")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\bi\b", "I", text)

    return text.strip()


def remove_words_for_svix(dict_payload: dict) -> dict:
    """
    Remove the words from the utterances for SVIX.

    Args:
        dict_payload (dict): The dict payload.

    Returns:
        dict: The dict payload with the words removed.
    """
    for utterance in dict_payload["utterances"]:
        utterance.pop("words", None)

    return dict_payload


def retrieve_user_platform() -> str:
    """
    Retrieve the user's platform.

    Returns:
        str: User's platform. Either 'linux', 'darwin' or 'win32'.
    """
    return sys.platform


async def save_file_locally(filename: str, file: "UploadFile") -> bool:
    """
    Save a file locally from an UploadFile object.

    Args:
        filename (str): The filename to save the file as.
        file (UploadFile): The UploadFile object.

    Returns:
        bool: Whether the file was saved successfully.
    """
    async with aiofiles.open(filename, "wb") as f:
        audio_bytes = await file.read()
        await f.write(audio_bytes)

    return True


def get_s3_client():
    def _retrieve_service(service, aws_creds):
        return boto3.client(
            service,
            aws_access_key_id=aws_creds.get("aws_access_key_id"),
            aws_secret_access_key=aws_creds.get("aws_secret_access_key"),
            region_name=aws_creds.get("region_name"),
        )

    s3_client = _retrieve_service(
        "s3",
        {
            "aws_access_key_id": settings.aws_access_key_id,
            "aws_secret_access_key": settings.aws_secret_access_key,
            "region_name": settings.aws_region_name,
        },
    )

    return s3_client


def upload_file(s3_client, file, bucket, object_name):
    try:
        s3_client.put_object(
            Body=file,
            Bucket=bucket,
            Key=object_name,
        )
    except Exception as e:
        logger.error(f"Exception while uploading results to S3: {e}")
        return False
    return True


async def send_update_with_svix(
    job_name: str,
    status: str,
    payload: dict,
    payload_retention_period: Optional[int] = 5,
) -> None:
    """
    Send the status update to Svix.

    Args:
        job_name (str): The name of the job.
        status (str): The status of the job.
        payload (dict): The payload to send.
        payload_retention_period (Optional[int], optional): The payload retention period. Defaults to 5.
    """
    if settings.svix_api_key and settings.svix_app_id:
        svix = SvixAsync(settings.svix_api_key)
        await svix.message.create(
            settings.svix_app_id,
            MessageIn(
                event_type=f"async_job.wordcab_transcribe.{status}",
                event_id=f"wordcab_transcribe_{status}_{job_name}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}",
                payload_retention_period=payload_retention_period,
                payload=payload,
            ),
        )
    else:
        logger.warning(
            "Svix API key and app ID are not set. Cannot send the status update to"
            " Svix."
        )

