from pydantic import BaseModel, Field, constr, validator, field_validator


class SignupBody(BaseModel):
    first_name: constr(strip_whitespace=True) 
    last_name: constr(strip_whitespace=True) 
    username: constr(strip_whitespace=True) 
    password: constr(strip_whitespace=True) 


class LoginBody(BaseModel):
    username: constr(strip_whitespace=True) 
    password: constr(strip_whitespace=True)