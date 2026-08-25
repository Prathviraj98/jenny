from pydantic import BaseModel, EmailStr
from typing import Optional, List

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str

class LoginPayload(BaseModel):
    username: str
    password: str

class UserProfileResponse(BaseModel):
    id: str
    email: str
    roles: List[str]
