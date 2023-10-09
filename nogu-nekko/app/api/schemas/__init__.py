from typing import Optional, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel

T = TypeVar('T')


def convert_to_optional(schema):
    return {k: Optional[v] for k, v in schema.__annotations__.items()}


class ModelBase(BaseModel):
    class Config:
        orm_mode = True


class APIException(HTTPException):
    def __init__(self, message: str, **kwargs):
        kwargs['message'] = message
        super().__init__(status_code=400, detail=kwargs)


class ModelResponse(BaseModel):
    identifier: str
    status: str
    data: Optional[BaseModel]
