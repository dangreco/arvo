from pydantic import BaseModel


class JwtConfig(BaseModel):
    secret: str
    algorithm: str
