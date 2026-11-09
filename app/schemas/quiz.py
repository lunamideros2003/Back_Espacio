from pydantic import BaseModel


class AnswerIn(BaseModel):
    id: int
    choice: int


class SubmitIn(BaseModel):
    answers: list[AnswerIn]
    level: str | None = None
