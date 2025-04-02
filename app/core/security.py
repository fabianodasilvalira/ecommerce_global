from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Configuração do algoritmo e tempo de expiração do token
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expira após 30 minutos
REFRESH_TOKEN_EXPIRE_DAYS = 7     # Token de refresh expira após 7 dias

# Criação de contexto para o hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criptografar a senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Função para verificar se a senha fornecida é válida
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar o token de acesso JWT
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Função para criar o token de refresh JWT
def create_refresh_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Função para verificar o token
def verify_token(token: str):
    credentials_exception = Exception("Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception
