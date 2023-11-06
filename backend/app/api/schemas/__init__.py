from typing import Optional, TypeVar

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar('T')


def convert_to_optional(schema):
    return {k: Optional[v] for k, v in schema.__annotations__.items()}


class ModelBase(BaseModel):
    class Config:
        orm_mode = True


class APIException(HTTPException):
    stored_kwargs = None
    def __init__(self, message: str, i18n_node: str, **kwargs):
        kwargs['message'] = message
        kwargs['i18n_node'] = 'exception.' + i18n_node
        self.stored_kwargs = kwargs
        super().__init__(status_code=400, detail=kwargs)
        
    def response(self, headers={'exception-source': 'internal'}):
        return JSONResponse(self.stored_kwargs, status_code=400, headers=headers)


class ModelResponse(BaseModel):
    identifier: str
    status: str
    data: Optional[BaseModel]
