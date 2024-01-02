class ForbiddenException(Exception):
    """ Forbidden exception 403"""
    pass


class TokenExpiredException(Exception):
    """ Token Expired """
    pass


class InvalidTokenException(Exception):
    """ Invalid Token """
    pass


class UserNotFoundException(Exception):
    """ User Not found """
    pass
