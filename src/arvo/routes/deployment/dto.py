from typing import Optional
from pydantic import BaseModel


class DeploymentCreateRequestDto(BaseModel):
    credential_id: int
    prompt: str


class DeploymentCreateResponseDto(BaseModel):
    id: int
    prompt: str
    status: str
    description: Optional[str]
    credential_id: int


class DeploymentGetResponseDto(BaseModel):
    id: int
    prompt: str
    status: str
    description: Optional[str]
    credential_id: int
