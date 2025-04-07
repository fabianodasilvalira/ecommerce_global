from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings

# 🔐 Configurações
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# 🔐 Contexto de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 Gera hash da senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 🔍 Verifica se a senha está correta
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 📦 Cria Access Token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔁 Cria Refresh Token
def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🧾 Decodifica token e valida
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "sub" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: 'sub' não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


# 🚀 Gera tokens com 'sub' automaticamente
def gerar_tokens(usuario_id: int, tipo_usuario: str = None) -> dict:
    payload = {"sub": str(usuario_id)}
    if tipo_usuario:
        payload["tipo_usuario"] = tipo_usuario

    access_token = create_access_token(data=payload)
    refresh_token = create_refresh_token(data=payload)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
