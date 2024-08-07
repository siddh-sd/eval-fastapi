from datetime import datetime, timedelta
from uuid import UUID
import jwt
from passlib.context import CryptContext
from config import ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_MINUTES,ALGORITHM,SECRET_KEY
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
  """
  Used to get hashed password.
  """
  return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
  """
  Used to verify password.
  """  
  return password_context.verify(password, hashed_pass)


def create_access_token(id: UUID, expires_time: int = None) -> str:
  """
  Used to create access token.
  """
  if expires_time is not None:
    expires_time = datetime.utcnow() + timedelta(minutes=expires_time)
  else:
    expires_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  
  to_encode = {"exp": expires_time, "id": str(id)}
  return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def create_refresh_token(id: UUID, expires_time: int = None) -> str:
  """
  Used to create refresh token.
  """
  if expires_time is not None:
    expires_time = datetime.utcnow() + timedelta(minutes=expires_time)
  else:
    expires_time = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
  
  to_encode = {"exp": expires_time,"id": str(id)}
  return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)