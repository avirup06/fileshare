import uuid
import hmac
import hashlib
import pyotp
from datetime import datetime, date

from fileshare.repositories.user_repository import UserRepository
from fileshare.models.user import User
from fileshare.common.logger import get_logger
from fileshare.common.enums import PasswordValidationStatus


logger = get_logger()


class UserService():
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user_by_id(self, id):
        model = self.repository.get(id)
        logger.info(model)
        return self.transform_from_model(model)
    
    def get_user_by_username(self, username):
        model = self.repository.get_user_by_user_name(username)
        return model

    def get_all_users(self):
        user_model_list = self.repository.get_all()
        return [self.transform_from_model(user) for user in user_model_list]

    def create_user(self, user):
        user['id'] = str(uuid.uuid4())
        salt = pyotp.random_base32()
        hash = (
                hmac.new(
                    salt.encode("UTF-8"), 
                    user['password'].encode(),
                    hashlib.sha256
                )
                .hexdigest()
            )
        user['salt'] = salt
        user['password_hash'] = hash
        user_model = User()
        self.transform_from_dict(user_model, user)
        model = self.repository.add(user_model)
        return model
        

    def validate_password(self, username: str, password: str):
        user: User = self.get_user_by_username(username)
        if not user:
            return PasswordValidationStatus.INVALID, None
        else:
            hash = (
                hmac.new(
                    user.salt.encode("UTF-8"),
                    password.encode(),
                    hashlib.sha256
                )
                .hexdigest()
            )
            if hmac.compare_digest(hash, user.password_hash):
                return PasswordValidationStatus.SUCCESS, user
            else:
                return PasswordValidationStatus.FAILED, None
    

    def fetch_user_files(self, model, date_serial=True, auto_deleted=False):
        def date_serial(obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            raise TypeError ("Type %s not serializable" % type(obj))
        
        if auto_deleted:
            f_list = [
                {
                    "id": file.id,
                    "filename": file.filename,
                    "code": file.code,
                    "created_on": date_serial(file.created_on) if date_serial else file.created_on,
                    "expiry_date": date_serial(file.expiry_date) if date_serial else file.expiry_date,
                    "is_deleted": file.is_deleted,
                    "is_auto_deleted": file.is_auto_deleted
                } 
                for file in model.files if auto_deleted if file.is_auto_deleted 
            ]
        else:
            f_list = [
                {
                    "id": file.id,
                    "filename": file.filename,
                    "code": file.code,
                    "created_on": date_serial(file.created_on) if date_serial else file.created_on,
                    "expiry_date": date_serial(file.expiry_date) if date_serial else file.expiry_date,
                    "is_deleted": file.is_deleted,
                    "is_auto_deleted": file.is_auto_deleted
                } 
                for file in model.files
            ]
        return f_list
    

    def transform_from_model(self, model: User):
        files_list = self.fetch_user_files(model)
        return {
            "id" : model.id,
            "first_name" : model.first_name,
            "last_name" : model.last_name,
            "username" : model.username,
            "files": files_list
        }

    def transform_from_dict(self, model: User, model_dict):

        if model_dict.get("id", None):
            model.id = model_dict["id"]
        if model_dict.get("first_name", None):
            model.first_name = model_dict["first_name"]
        if model_dict.get("last_name", None):
            model.last_name = model_dict["last_name"]
        if model_dict.get("username", None):
            model.username = model_dict["username"]
        if model_dict.get("salt", None):
            model.salt = model_dict["salt"]
        if model_dict.get("password_hash", None):
            model.password_hash = model_dict["password_hash"]
        
        