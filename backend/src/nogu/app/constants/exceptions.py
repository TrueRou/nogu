from fastapi import HTTPException
from fastapi.responses import JSONResponse


class APIException(HTTPException):
    stored_kwargs = None

    def __init__(self, message: str, i18n_node: str, status_code: int, settled: bool = True, **kwargs):
        kwargs["message"] = message
        kwargs["i18n_node"] = "exception." + i18n_node
        kwargs["settled"] = settled
        self.stored_kwargs = kwargs
        super().__init__(status_code=status_code, detail=kwargs)

    def extends(self, next_node: dict) -> "APIException":
        self.stored_kwargs["details"] = next_node
        return self

    def response(self, headers={"exception-source": "internal"}):
        return JSONResponse(self.stored_kwargs, status_code=self.status_code, headers=headers)
