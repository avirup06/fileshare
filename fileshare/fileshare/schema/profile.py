from pydantic import BaseModel, Field, constr, EmailStr
from typing import Optional,Any
from datetime import datetime


class UserBody(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str

    meta: dict = None

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        """
            Override the default dict method to exclude None values in the response
        """
        kwargs.pop('exclude_none', None)
        return super().model_dump(*args, exclude_none=True, **kwargs)

