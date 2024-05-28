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
"""Audio url endpoint for the Wordcab Transcribe API."""
import json
import asyncio
import shortuuid
from typing import Optional

from loguru import logger
from fastapi import status as http_status
from fastapi import APIRouter, BackgroundTasks

from my_project.config import settings
from my_project.dependencies import service, download_limit
from my_project.models import ExampleRequest, ExampleResponse
from my_project.utils import (
    get_s3_client,
    upload_file,
    send_update_with_svix,
)

router = APIRouter()

s3_client = get_s3_client()


@router.post("", status_code=http_status.HTTP_202_ACCEPTED)
async def inference_with_audio_url(
    background_tasks: BackgroundTasks,
    url: str,
    send_to_s3: bool = False,
    send_to_svix: bool = False,
    data: Optional[ExampleRequest] = None,
) -> dict:
    """Inference endpoint with audio url."""
    uuid = f"audio_url_{shortuuid.ShortUUID().random(length=32)}"
    data = ExampleRequest() if data is None else ExampleRequest(**data.dict())

    async def process_audio():
        try:
            async with download_limit:
                # fill in

                # background_tasks.add_task(function, param=param)

                task = asyncio.create_task(
                    service.process_input()
                )

                result = await task
                result = ExampleResponse()

                if send_to_s3:
                    upload_file(
                        s3_client,
                        file=bytes(json.dumps(result.model_dump()).encode("UTF-8")),
                        bucket=settings.aws_storage_bucket_name,
                        object_name=f"responses/{data.task_token}_{data.job_name}.json",
                    )

                # background_tasks.add_task(function, param=param)

                if send_to_svix:
                    await send_update_with_svix(
                        data.job_name,
                        "finished",
                        {
                            "job_name": data.job_name,
                            "task_token": data.task_token,
                        },
                    )
        except Exception as e:
            error_message = f"Error during transcription: {e}"
            logger.error(error_message)

            if send_to_svix:
                error_payload = {
                    "error": error_message,
                    "job_name": data.job_name,
                    "task_token": data.task_token,
                }

                await send_update_with_svix(data.job_name, "error", error_payload)

    # Add the process_audio function to background tasks
    background_tasks.add_task(process_audio)

    # Return the job name and task token immediately
    return {"job_name": data.job_name, "task_token": data.task_token}

