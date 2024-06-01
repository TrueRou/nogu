from fastapi import HTTPException
from fastapi.responses import JSONResponse


class APIException(HTTPException):
    stored_kwargs = None

    def __init__(self, message: str, i18n_node: str, **kwargs):
        kwargs["message"] = message
        kwargs["i18n_node"] = "exception." + i18n_node
        self.stored_kwargs = kwargs
        super().__init__(status_code=400, detail=kwargs)

    def extends(self, next_node: dict) -> "APIException":
        self.stored_kwargs["details"] = next_node
        return self

    def response(self, headers={"exception-source": "internal"}):
        return JSONResponse(self.stored_kwargs, status_code=400, headers=headers)


glob_validation = APIException(f"Validation error ", "glob.validation")
glob_internal = APIException("Backend server error.", "glob.internal")
glob_not_exist = APIException("Resources not found.", "glob.not-exist")
glob_no_permission = APIException("No permission.", "glob.no-permission")
glob_not_belongings = APIException("Resources not belongs to you.", "glob.not-belongings")
