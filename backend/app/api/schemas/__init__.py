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
        
    def extends(self, next_node: dict) -> 'APIException':
        self.stored_kwargs['details'] = next_node
        return self
        
    def response(self, headers={'exception-source': 'internal'}):
        return JSONResponse(self.stored_kwargs, status_code=400, headers=headers)

class APIExceptions:
    # Glob
    glob_validation = APIException(f'Validation error ', 'glob.validation')
    glob_internal = APIException('Backend server error.', 'glob.internal')
    glob_not_exist = APIException('Resources not found.', 'glob.not-exist')
    
    # User:
    user_unauthorized = APIException('Unauthorized.', 'user.unauthorized')
    user_duplicated = APIException('User already exists.', 'user.duplicated')
    user_username_illegal = APIException('Username illegal.', 'user.username.illegal')
    user_password_illegal = APIException('Password illegal.', 'user.password.illegal')
    user_country_illegal = APIException('Country illegal.', 'user.country.illegal')
    user_credentials_incorrect = APIException('Incorrect username or password.', 'user.credentials.incorrect')
    user_email_duplicated = APIException('Email already exists.', 'user.email.duplicated')
   
    # Team:
    team_not_exist = APIException(message="Team not found.", i18n_node="team.not-exist")
    team_not_belongings = APIException(message="You are not a member of the team.", i18n_node="team.not-belongings")
    team_active_stage_not_exist = APIException(message="Team has no active stage.", i18n_node="team.active_stage.not-exist")
    
    # Stage:
    stage_not_exist = APIException(message="Stage not found.", i18n_node="stage.not-exist")
    
    # Score:
    score_not_exist = APIException(message="Score not found.", i18n_node="score.not-exist")
    score_not_belongings = APIException(message="Score not belongs to you.", i18n_node="score.not-belongings")

    # Beatmap:
    beatmap_not_exist = APIException(message="Beatmap not found.", i18n_node="beatmap.not-exist")

class ModelResponse(BaseModel):
    identifier: str
    status: str
    data: Optional[BaseModel]
