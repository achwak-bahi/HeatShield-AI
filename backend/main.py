from pathlib import Path
import sys

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
# Pour importer src/prediction/predict.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.prediction.predict import predict_risk

from .database import Base, engine, get_db
from .models import User, Prediction
from .schemas import UserCreate, UserLogin, Token, UserResponse, PredictionResponse
from .auth import hash_password, verify_password, create_access_token, decode_access_token


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HeatShield AI API",
    description="API MVP pour HeatShield AI",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class PredictionRequest(BaseModel):
    temp_max: float
    humidity: float
    wind_max: float
    rain: float
    et0: float
    vpd_max: float
    radiation: float
    temp_min: float | None = None
    temp_mean: float | None = None
    consecutive_hot_days_38: int = 0


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )

    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur introuvable"
        )

    return user


@app.get("/")
def root():
    return {"message": "Bienvenue sur HeatShield AI API"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email ou username déjà utilisé"
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")

    access_token = create_access_token(data={"sub": user.email, "role": user.role})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/predict", response_model=PredictionResponse)
def predict(
    data: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = predict_risk(
        temp_max=data.temp_max,
        humidity=data.humidity,
        wind_max=data.wind_max,
        rain=data.rain,
        et0=data.et0,
        vpd_max=data.vpd_max,
        radiation=data.radiation,
        temp_min=data.temp_min,
        temp_mean=data.temp_mean,
        consecutive_hot_days_38=data.consecutive_hot_days_38
    )

    new_prediction = Prediction(
        user_id=current_user.id,

        temp_max=data.temp_max,
        humidity=data.humidity,
        wind_max=data.wind_max,
        rain=data.rain,
        et0=data.et0,
        vpd_max=data.vpd_max,
        radiation=data.radiation,
        consecutive_hot_days_38=data.consecutive_hot_days_38,

        probability_high_risk=result["probability_high_risk"],
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        confidence=result["confidence"],
        model_name=result["model_name"]
    )

    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return new_prediction


@app.get("/predictions/history", response_model=list[PredictionResponse])
def get_prediction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    predictions = (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )

    return predictions