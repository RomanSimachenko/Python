class NoInternetConnectionException(Exception):
    """You have no internet connection"""


class CantAuthenticateException(Exception):
    """Program can't authenticate in some site"""


class InvalidLoginData(Exception):
    """Invalid login or password in some site"""


class VerificationFailedException(Exception):
    """Program can't verificate something"""
