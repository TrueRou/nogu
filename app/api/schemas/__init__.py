from typing import Optional, Generic, TypeVar

from pydantic import BaseModel, validator

T = TypeVar('T')


def convert_to_optional(schema):
    return {k: Optional[v] for k, v in schema.__annotations__.items()}


class ModelBase(BaseModel):
    class Config:
        orm_mode = True


class APIResponse:
    def __init__(self, success=True, info="", **kwargs):
        self.success = success
        if info != "":
            self.info = info
        for key in kwargs.keys():
            self.__setattr__(key, kwargs[key])


def docs(obj):
    return {200: {"model": obj}}
