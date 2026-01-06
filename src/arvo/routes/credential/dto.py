from pydantic import BaseModel


class CredentialCreateRequestDto(BaseModel):
    name: str


class AWSCredentialCreateRequestDto(CredentialCreateRequestDto):
    region: str
    access_key_id: str
    secret_access_key: str


class AWSCredentialCreateResponseDto(BaseModel):
    id: int
    name: str
