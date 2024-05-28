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
"""Sync endpoint."""

import asyncio
from typing import List, Union

from loguru import logger
from fastapi import status as http_status
from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile

from my_project.dependencies import service
from my_project.models import ExampleRequest, ExampleResponse
from my_project.services.example_service import ProcessException
from my_project.utils import *

router = APIRouter()


@router.post(
    "", response_model=Union[ExampleResponse, str], status_code=http_status.HTTP_200_OK
)
async def inference_with_audio(  # noqa: C901
    background_tasks: BackgroundTasks,
    batch_size: Union[int, None] = Form(None),  # noqa: B008
    offset_start: Union[float, None] = Form(None),  # noqa: B008
    offset_end: Union[float, None] = Form(None),  # noqa: B008
    num_speakers: int = Form(-1),  # noqa: B008
    diarization: bool = Form(False),  # noqa: B008
    multi_channel: bool = Form(False),  # noqa: B008
    source_lang: str = Form("en"),  # noqa: B008
    timestamps: str = Form("s"),  # noqa: B008
    vocab: Union[List[str], None] = Form(None),  # noqa: B008
    word_timestamps: bool = Form(False),  # noqa: B008
    internal_vad: bool = Form(False),  # noqa: B008
    repetition_penalty: float = Form(1.2),  # noqa: B008
    compression_ratio_threshold: float = Form(2.4),  # noqa: B008
    log_prob_threshold: float = Form(-1.0),  # noqa: B008
    no_speech_threshold: float = Form(0.6),  # noqa: B008
    condition_on_previous_text: bool = Form(True),  # noqa: B008
    file: UploadFile = File(...),  # noqa: B008
) -> ExampleResponse:
    """Inference endpoint with audio file."""

    data = ExampleRequest(
        offset_start=offset_start,
        offset_end=offset_end,
        num_speakers=num_speakers,
        diarization=diarization,
        batch_size=batch_size,
        source_lang=source_lang,
        timestamps=timestamps,
        vocab=vocab,
        word_timestamps=word_timestamps,
        internal_vad=internal_vad,
        repetition_penalty=repetition_penalty,
        compression_ratio_threshold=compression_ratio_threshold,
        log_prob_threshold=log_prob_threshold,
        no_speech_threshold=no_speech_threshold,
        condition_on_previous_text=condition_on_previous_text,
        multi_channel=multi_channel,
    )

    try:
        # something with data
        pass

    except Exception as e:
        raise HTTPException(  # noqa: B904
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Process failed: {e}",
        )

    # background_tasks.add_task(function, param=param)

    task = asyncio.create_task(
        service.process_input()
    )
    result = await task

    # background_tasks.add_task(function, param=param)

    if isinstance(result, ProcessException):
        logger.error(result.message)
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(result.message),
        )
    else:
        return ExampleResponse()
