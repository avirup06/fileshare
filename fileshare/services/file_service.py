import uuid
from typing import List
from datetime import date
import os

from fileshare.repositories.file_repository import FileRepository
from fileshare.models.file import File
from fileshare.common.logger import get_logger

logger = get_logger()


class FileService():
    def __init__(self, repository: FileRepository):
        self.repository = repository

    def get_file_by_id(self, id):
        model = self.repository.get(id)
        logger.info(model)
        return model
    
    def get_file_by_code(self, code):
        model = self.repository.get_file_by_code(code)
        return model

    def create_file(self, file):
        file['id'] = str(uuid.uuid4())
        
        file_model = File()
        self.transform_from_dict(file_model, file)
        model = self.repository.add(file_model)
        return model

    def update_file(self, file: File):
        self.repository.update(
            id=file.id, 
            model=self.transform_from_model(file)
        )
        return file
    
    def update_files_on_expiry(self, file_list: List[File]):
        for file in file_list:
                if not file.is_auto_deleted:
                    if file.expiry_date < date.today():
                        file.is_auto_deleted = True
                        self.update_file(file)
    
    def delete_file_from_storage(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise Exception("file does not exist in storage")
    
    def transform_from_model(self, model: File):
        return {
            "id" : model.id,
            "filename" : model.filename,
            "code" : model.code,
            "created_on" : model.created_on,
            "expiry_date": model.expiry_date,
            "is_deleted": model.is_deleted,
            "is_auto_deleted": model.is_auto_deleted,
            "user_id": model.user_id
        }

    def transform_from_dict(self, model: File, model_dict):

        if model_dict.get("id", None):
            model.id = model_dict["id"]
        if model_dict.get("filename", None):
            model.filename = model_dict["filename"]
        if model_dict.get("code", None):
            model.code = model_dict["code"]
        if model_dict.get("created_on", None):
            model.created_on = model_dict["created_on"]
        if model_dict.get("expiry_date", None):
            model.expiry_date = model_dict["expiry_date"]
        if model_dict.get("is_deleted", None):
            model.is_deleted = model_dict["is_deleted"]
        if model_dict.get("is_auto_deleted", None):
            model.is_auto_deleted = model_dict["is_auto_deleted"]
        if model_dict.get("user_id", None):
            model.user_id = model_dict["user_id"]
        
        