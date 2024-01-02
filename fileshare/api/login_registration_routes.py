import traceback
from functools import lru_cache

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fileshare.db import get_db
from fileshare.repositories.user_repository import UserRepository
from fileshare.services.user_service import UserService
from fileshare.common.enums import PasswordValidationStatus
from fileshare.common.utility import response_helper
from fileshare.common.auth.jwt_token import create_jwt_token
from fileshare.schema.login_registration import LoginBody, SignupBody
from fileshare.common.logger import get_logger


router = APIRouter()
logger = get_logger()


@lru_cache
def get_user_service(session):
    user_repository = UserRepository(session)
    user_service = UserService(user_repository)
    return user_service


@router.post("/signup")
async def signup(signup_body: SignupBody, session: Session = Depends(get_db)):
    user_service = get_user_service(session)
    logger.info(f"signup successful - user id: {signup_body.username}")
    try:
        created_user = user_service.create_user(signup_body.model_dump())
        if created_user:
            user_dict = user_service.transform_from_model(created_user)
            user_dict.pop('files')
            return response_helper(
                data={
                        "token": create_jwt_token(user_dict)
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


@router.post("/login")
async def login(auth_body: LoginBody, session: Session = Depends(get_db)):
    user_service = get_user_service(session)
    try:
        logger.info(f"login attempt - user id: {auth_body.username}")
        res, user = user_service.validate_password(
            username=auth_body.username,
            password=auth_body.password
        )
        if res == PasswordValidationStatus.SUCCESS:
            user_dict = user_service.transform_from_model(user)
            user_dict.pop('files')
            logger.info(f"login successful - user id: {auth_body.username}")
            return response_helper(
                data={
                    "token": create_jwt_token(user_dict)
                },
                msg='Success',
                status_code=200
            )
        elif res == PasswordValidationStatus.FAILED:
            logger.info(f"login failed - user id: {auth_body.username}")
            return response_helper(
                data='Invalid password',
                msg='Failed',
                status_code=500
            )
        else:
            logger.info(f"login failed - invalid user id: {auth_body.username}")
            return response_helper(
                data='Invalid username',
                msg='Failed',
                status_code=500
            )
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return response_helper(
                data='',
                msg='Internal sever error',
                status_code=500,
                exception=True
            )