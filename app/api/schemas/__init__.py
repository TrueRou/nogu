from typing import Optional, Generic, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel, validator

T = TypeVar('T')


def convert_to_optional(schema):
    return {k: Optional[v] for k, v in schema.__annotations__.items()}


class ModelBase(BaseModel):
    class Config:
        orm_mode = True


class APIResponse:
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self.__setattr__(key, kwargs[key])


class APIException(HTTPException):
    def __init__(self, info: str, **kwargs):
        kwargs['info'] = info
        super().__init__(status_code=500, detail=kwargs)


def docs(obj):
    return {200: {"model": obj}}
