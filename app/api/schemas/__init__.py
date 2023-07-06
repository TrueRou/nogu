from typing import Optional

from pydantic import BaseModel


def convert_to_optional(schema):
    return {k: Optional[v] for k, v in schema.__annotations__.items()}


class ModelBase(BaseModel):
    class Config:
        orm_mode = True
