class WalletException(Exception):
    err_code = 500


class UserNotFound(WalletException):
    err_code = 404


class UserExists(WalletException):
    err_code = 409


class WalletNotFound(WalletException):
    err_code = 404


class WalletExists(WalletException):
    err_code = 409
