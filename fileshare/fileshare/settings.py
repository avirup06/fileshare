from pydantic_settings import BaseSettings
import yaml
import pathlib
import os
from dotenv import load_dotenv, find_dotenv
from enum import Enum


class DBSettings(BaseSettings):
    USERNAME: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str
    class Config:
        case_sensitive = True

class SMSSettings(BaseSettings):
    ACCOUNT_SID: str
    TOKEN: str
    MESSAGE_SERVICE_SID: str
    NUMBER: str
    class Config:
        case_sensitive = True

class OCISetting(BaseSettings):
    BUCKET_NAME:str 
    CONFIG_PATH:str     
    class Config:
        case_sensitive = True

class LOGSetting(BaseSettings):
    LOG_PATH:str
    class Config:
        case_sensitive = True


class ConfigType(Enum):
    DB = DBSettings
    SMS = SMSSettings
    OCI = OCISetting
    LOG = LOGSetting


def get_config():
    with open(os.path.join(pathlib.Path(__file__).parent.resolve(), 'config.yaml'), '+r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    
    # os.environ['env_type'] = 'DEV'
    if not os.environ.get('stage'):
        load_dotenv(find_dotenv())
    config = data.get(os.environ.get('stage'))
    return config


def get_db_config():
    config = get_config().get('DB')
    settings = DBSettings(**config)
    return settings

def get_sms_config():
    config = get_config().get('SMS')
    settings = SMSSettings(**config)
    return settings

def get_oci_config():
    config = get_config().get('OCI')
    settings = OCISetting(**config)
    return settings

def get_log_config():
    config = get_config().get('LOG')
    settings = LOGSetting(**config)
    return settings

# def get_db_config():
#     config = get_config().get('DATABASE')
#     settings = DBSettings(**config)
#     return settings

# def get_sms_config():
#     config = get_config().get('SMS')
#     settings = SMSSettings(**config)
#     return settings

# def get_oci_config():
#     config = get_config().get('OCI')
#     settings = OCISetting(**config)
#     return settings

def get_config_type(type: ConfigType):
    config = get_config().get(type.name)
    settings = type.value(**config)
    return settings