from rest_framework.exceptions import APIException

from libs.error_reports import send_manually_error_email


class AlreadyExistsException(APIException):
    status_code = 409
    default_detail = "Already Exists"


class InvalidInputDataException(APIException):
    status_code = 400
    default_detail = "Invalid Input Data"

    def __init__(self, message=None, *args, **kwargs):
        send_manually_error_email(message)
        super(InvalidInputDataException, self).__init__(*args, **kwargs)


class VerificationException(APIException):
    status_code = 400
    default_detail = "User Not Verified"


class InvalidVerificationCodeException(APIException):
    status_code = 400
    default_detail = "Invalid Verification Data"


class InvalidCredentialsException(APIException):
    status_code = 401
    default_detail = "Invalid Credentials"


class UserNotAllowedException(APIException):
    status_code = 401
    default_detail = "User Not Allowed"


class UserExistsException(AlreadyExistsException):
    default_detail = "User Already Exists"


class UserDoesNotExistsException(APIException):
    status_code = 404
    default_detail = "User Does Not Exists"
