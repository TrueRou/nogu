import datetime
from sqlmodel import Field, SQLModel


class AstConditionPublic(SQLModel):
    name: str
    description: str | None


class AstCondition(SQLModel, table=True):
    __tablename__ = "ast_conditions"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    description: str | None
    ast_expression: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    user_id: int = Field(foreign_key="users.id")
