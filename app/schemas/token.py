from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    user_id: int
    role: str

class LoginRequest(BaseModel):
    email: str
    password: str
