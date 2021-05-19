class WalletException(Exception):
    status_code = 500


class UserNotFound(WalletException):
    status_code = 404


class UserExists(WalletException):
    status_code = 409


class WalletNotFound(WalletException):
    status_code = 404


class WalletExists(WalletException):
    status_code = 409


class InsufficientBalance(WalletException):
    status_code = 409
