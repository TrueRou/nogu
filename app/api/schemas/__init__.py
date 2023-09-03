import json
from typing import Optional, Generic, TypeVar

from fastapi import HTTPException
from orjson import orjson
from pydantic import BaseModel, validator

T = TypeVar('T')


def convert_to_optional(schema):
    return {k: Optional[v] for k, v in schema.__annotations__.items()}


class ModelBase(BaseModel):
    class Config:
        orm_mode = True


class APIResponse:
    dict_keys = []

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self.__setattr__(key, kwargs[key])
            self.dict_keys.append(key)

    def keys(self):
        return self.dict_keys

    def __getitem__(self, item):
        item = getattr(self, item)
        return item.dict() if isinstance(item, ModelBase) else item

    def dict(self):
        result = {}
        for key in self.dict_keys:
            item = self.__getattribute__(key)
            result[key] = item.dict() if isinstance(item, ModelBase) else item
        return result


class APIException(HTTPException):
    def __init__(self, info: str, **kwargs):
        kwargs['info'] = info
        super().__init__(status_code=500, detail=kwargs)


class ModelResponse(BaseModel):
    identifier: str
    status: str
    data: Optional[BaseModel]


def docs(obj):
    return {200: {"model": obj}}
