from pydantic import BaseModel


class GetUserResponseDto(BaseModel):
    id: int
    email: str
