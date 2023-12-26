import logging
import os
import shutil
from logging.config import dictConfig

from app.core.config import log_config_settings, settings
from fastapi import HTTPException, UploadFile

dictConfig(log_config_settings.dict())
logger = logging.getLogger("mitinapp")


def validate_and_upload_image(image_file: UploadFile):

    if image_file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail=f"File type of {image_file.content_type} is not supported",
        )

    # TODO: improve, not high performant
    image_size_mb = len(image_file.file.read()) / 1000000
    image_file.file.seek(0)  # needed after call read()

    if image_size_mb > 5:  # 5MB
        logger.info(f"image size: {image_size_mb} MB")
        raise HTTPException(
            status_code=400,
            detail=f"File is too big",
        )
    # Copy image to static folder
    filename = image_file.filename.replace(' ', '')
    url = settings.MEDIA_FOLDER + filename
    with open(url, "wb") as image:
        shutil.copyfileobj(image_file.file, image)
    return filename
