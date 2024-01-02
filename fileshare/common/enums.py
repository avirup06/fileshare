from enum import Enum


class PasswordValidationStatus(Enum):
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    ERROR = 'ERROR'
    INVALID = 'INVALID'
