from fastapi import HTTPException
from fastapi.responses import JSONResponse


class APIException(HTTPException):
    stored_kwargs = None

    def __init__(self, message: str, i18n_node: str, error_code: int, **kwargs):
        kwargs["message"] = message
        kwargs["i18n_node"] = "exception." + i18n_node
        kwargs["error_code"] = error_code
        self.stored_kwargs = kwargs
        super().__init__(status_code=400, detail=kwargs)

    def extends(self, next_node: dict) -> "APIException":
        self.stored_kwargs["details"] = next_node
        return self

    def response(self, headers={"exception-source": "internal"}):
        return JSONResponse(self.stored_kwargs, status_code=400, headers=headers)


glob_validation = APIException(f"Validation error ", "glob.validation")
glob_no_permission = APIException("No permission.", "glob.no-permission")
glob_not_belongings = APIException("Not belongings.", "glob.not-belongings")
