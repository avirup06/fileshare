from sqlalchemy.orm.query import Query
from sqlalchemy import desc

from fileshare.models.file import File
from fileshare.common.base_repository import Repository


class FileRepository(Repository):
    def __init__(self, session):
        self.session = session
        self.model_type = File

    def get_file_by_code(self, code):
        with self.session as session:
            return (
                session.query(self.model_type)
                .filter_by(code=code)
                .first()
            )