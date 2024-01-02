import traceback
import os
from functools import lru_cache
import threading

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fileshare.db import get_db
from fileshare.models.user import User
from fileshare.repositories.user_repository import UserRepository
from fileshare.services.user_service import UserService
from fileshare.models.file import File as FileModel
from fileshare.repositories.file_repository import FileRepository
from fileshare.services.file_service import FileService
from fileshare.common.auth.jwt_token import JWTBearer
from fileshare.common.utility import response_helper
from fileshare.common.logger import get_logger


router = APIRouter()
path = os.environ.get('storage')
logger = get_logger()


@lru_cache
def get_user_service(session):
    user_repository = UserRepository(session)
    user_service = UserService(user_repository)
    return user_service

@lru_cache
def get_file_service(session):
    file_repository = FileRepository(session)
    file_service = FileService(file_repository)
    return file_service


@router.get("/profile")
async def current_user_details(current_user = Depends(JWTBearer()), session: Session = Depends(get_db)):
    logger.info(f"get profile - user id: {current_user.get('id')}")
    try:
        user_service = get_user_service(session)
        file_service = get_file_service(session)
        user = user_service.get_user_by_username(current_user.get("username"))
        if user is not None:
            thread = threading.Thread(
                target=file_service.update_files_on_expiry(user.files)
            )
            thread.start()
            thread.join()
            user_details = user_service.transform_from_model(user)
            return response_helper(
                data=user_details,
                msg='Success',
                status_code=200
            )
        else:
            logger.error(f"user not found - user id: {current_user.get('id')}")
            return response_helper(
                data='user deatails not found',
                msg='Failed',
                status_code=400
            )
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return response_helper(
            data=str(e),
            msg='Internal sever error',
            status_code=500,
            exception=True
        )

@router.get("/files")
async def user_files(auto_deleted: bool = None, current_user = Depends(JWTBearer()), session: Session = Depends(get_db)):
    try:
        logger.info(f"view files - user id: {current_user.get('id')}")
        file_service = get_file_service(session)
        user_service = get_user_service(session)
        user = user_service.get_user_by_username(current_user.get("username"))
        thread = threading.Thread(
            target=file_service.update_files_on_expiry(user.files)
        )
        thread.start()
        thread.join()
        files_list = user_service.fetch_user_files(user, auto_deleted=auto_deleted)

        return response_helper(
                data=files_list,
                msg='Success',
                status_code=200
            )
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return response_helper(
            data=str(e),
            msg='Internal sever error',
            status_code=500,
            exception=True
        )

@router.delete("/files")
async def delete_user_files(file_id: str, current_user = Depends(JWTBearer()), session: Session = Depends(get_db)):
    try:
        logger.info(f"delete file started - user id: {current_user.get('id')} - file id: {file_id}")
        file_service = get_file_service(session)
        file: FileModel = file_service.get_file_by_id(file_id)

        if file.user_id is not current_user.get('id'):
            logger.info(f"user attempted to delete files owned by other user - user id: {current_user.get('id')} - file id: {file_id}")
            return response_helper(
                    data=f'cannot delete file owned by other user',
                    msg='Failed',
                    status_code=200
                )
        if file:
            if file.is_deleted:
                logger.info(f"delete file failed, already deleted - user id: {current_user.get('id')} - file id: {file_id}")
                return response_helper(
                    data=f'File: {file.filename} already deleted',
                    msg='Success',
                    status_code=200
                )
            file_path = f'{path}\{file.code}.{(file.filename).rsplit(".", 1)[1]}'
            file.is_deleted = True
            file_service.update_file(file)
            file_service.delete_file_from_storage(file_path)
            logger.info(f"delete file successful - user id: {current_user.get('id')} - file id: {file_id}")
            return response_helper(
                data=f'File: {file.filename} deleted',
                msg='Success',
                status_code=201
            )
        else:
            logger.error(f"file not found - user id: {current_user.get('id')} - file id: {file_id}")
            return response_helper(
                data='file not found',
                msg='Failed',
                status_code=200
            )
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return response_helper(
            data=str(e),
            msg='Internal sever error',
            status_code=500,
            exception=True
        )
    
