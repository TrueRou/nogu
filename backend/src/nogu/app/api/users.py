from fastapi import APIRouter, status
from starlette.exceptions import HTTPException
from fastapi_users.router.common import ErrorCode
from nogu.app.constants.exceptions import APIException

router = APIRouter()

user_password_illegal = APIException("Password illegal.", "user.password.illegal", status_code=status.HTTP_400_BAD_REQUEST)
user_unauthorized = APIException("Unauthorized.", "user.unauthorized", status_code=status.HTTP_401_UNAUTHORIZED)
user_duplicated = APIException("User already exists.", "user.duplicated", status_code=status.HTTP_400_BAD_REQUEST)
user_credentials_incorrect = APIException("Incorrect username or password.", "user.credentials.incorrect", status_code=status.HTTP_400_BAD_REQUEST)
user_email_duplicated = APIException("Email already exists.", "user.email.duplicated", status_code=status.HTTP_400_BAD_REQUEST)
user_internal = APIException("Backend server error.", "user.internal", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
user_not_exist = APIException("Resources not found.", "user.not-exist", status_code=status.HTTP_404_NOT_FOUND)


def parse_exception(exception: HTTPException) -> APIException:
    if exception.status_code == 500:
        return user_internal
    if exception.status_code == 401:
        return user_unauthorized
    if exception.status_code == 404:
        return user_not_exist
    if exception.status_code == 400:
        if type(exception.detail) == dict:
            if exception.detail["code"] in [
                ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                ErrorCode.REGISTER_INVALID_PASSWORD,
                ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
            ]:
                next_node = {"message": exception.detail["reason"]}
                return user_password_illegal.extends(next_node)
        if exception.detail == ErrorCode.REGISTER_USER_ALREADY_EXISTS:
            return user_duplicated
        if exception.detail in [
            ErrorCode.LOGIN_BAD_CREDENTIALS,
            ErrorCode.RESET_PASSWORD_BAD_TOKEN,
        ]:
            return user_credentials_incorrect
        if exception.detail == ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS:
            return user_email_duplicated


from nogu.app.models.user import UserSrv

router.include_router(UserSrv.user_router, prefix="/users", tags=["users"])
router.include_router(UserSrv.auth_router, prefix="/auth/jwt", tags=["auth"])
router.include_router(UserSrv.register_router, prefix="/auth", tags=["auth"])
