from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

from datetime import datetime


class PredictionResponse(BaseModel):
    id: int
    temp_max: float
    humidity: float
    wind_max: float
    rain: float
    et0: float
    vpd_max: float
    radiation: float
    consecutive_hot_days_38: int

    probability_high_risk: float
    risk_score: float
    risk_level: str
    confidence: float
    model_name: str

    created_at: datetime

    class Config:
        from_attributes = True