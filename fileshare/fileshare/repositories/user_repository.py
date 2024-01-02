from sqlalchemy.orm.query import Query
from sqlalchemy import desc

from fileshare.models.user import User
from fileshare.common.base_repository import Repository


class UserRepository(Repository):
    def __init__(self, session):
        self.session = session
        self.model_type = User

    def get_user_by_user_name(self, username):
        with self.session as session:
            return (
                session.query(self.model_type)
                .filter_by(username=username)
                .first()
            )