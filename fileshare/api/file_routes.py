import traceback
from functools import lru_cache
import os
import pathlib
from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Body
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from secrets import token_hex

from fileshare.db import get_db
from fileshare.common.auth.jwt_token import JWTBearer
from fileshare.repositories.file_repository import FileRepository
from fileshare.services.file_service import FileService
from fileshare.models.file import File as FileModel
from fileshare.common.utility import response_helper
from fileshare.common.logger import get_logger


router = APIRouter()
path = os.environ.get('storage')
CHUNK_SIZE = 1024 * 1024
logger = get_logger()


@lru_cache
def get_file_service(session):
    file_repository = FileRepository(session)
    file_service = FileService(file_repository)
    return file_service


@router.post("/check")
async def check(
        current_user = Depends(JWTBearer())
    ):
    # user_id = current_user.get('id')
    return response_helper(
        data={
            # 'id': user_id
            "id": "123"
        },
        msg='Success',
        status_code=200
    )


@router.post("/upload")
async def upload(
        expiry_date: Annotated[date, Body(embed=True)], file: UploadFile = File(...), 
        current_user = Depends(JWTBearer()), session: Session = Depends(get_db)
    ):
    logger.info(f"file upload started - user id: {current_user.get('id')}")
    file_service =  get_file_service(session)
    try:
        user_id = current_user.get("id")
        file_ext = file.filename.split('.').pop()
        file_name = token_hex(10)
        file_path = f'{path}\{file_name}.{file_ext}'
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        file_dict = {
            "filename": file.filename,
            "code": file_name,
            "created_on": datetime.now(),
            "expiry_date": expiry_date,
            "user_id": user_id
        }
        created_file_model: FileModel = file_service.create_file(file_dict)
        logger.info(f"file upload successful - user id: {current_user.get('id')}")
        return response_helper(
            data={
                "file code": created_file_model.code
            },
            msg='Success',
            status_code=201
        )
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return response_helper(
            data='Failed',
            msg=f'{str(e)}',
            status_code=500,
            exception=True
        )


@router.get("/download")
async def download(file_code: str, current_user = Depends(JWTBearer()), session: Session = Depends(get_db)):
    file_service =  get_file_service(session)
    logger.info(f"file download started - user id: {current_user.get('id')} - file_code: {file_code}")
    try:
        file: FileModel = file_service.get_file_by_code(file_code)
        if file.is_deleted:
            logger.info(f"file download failed, file deleted by owner - file_code: {file_code}")
            return response_helper(
                data='file deleted by owner',
                msg='Success',
                status_code=200,
        )
        elif file.expiry_date < date.today():
            if not file.is_auto_deleted:
                file.is_auto_deleted = True
                file_service.update_file(file)
                logger.info(f"file download failed, file expired - file_code: {file_code}")
            return response_helper(
                data='file expired',
                msg='Success',
                status_code=200,
        )
        else:
            file_path = f'{path}\{file.code}.{(file.filename).rsplit(".", 1)[1]}'
            def iterfile():
                with open(file_path, 'rb') as f:
                    while chunk := f.read(CHUNK_SIZE):
                        yield chunk
            
            media_type = 'application/octet-stream'
            headers = {
                'Content-Disposition': f'attachment; filename="{file.filename}" '
            }
            if file.filename.endswith('.pdf'):
                media_type = 'application/pdf'
            
            logger.info(f"file download successfull - user id: {current_user.get('id')} - file_code: {file_code}")
            return StreamingResponse(
                iterfile(), 
                headers=headers,
                media_type=media_type
            )

    except Exception as e:
        logger.error(str(e), exc_info=True)
        return response_helper(
            data='Failed',
            msg=f'{str(e)}',
            status_code=500,
            exception=True
        )