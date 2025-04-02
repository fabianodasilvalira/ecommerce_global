from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.usuario import Usuario, TipoUsuarioEnum
from app.core.security import (
    hash_password, verify_password, create_access_token, create_refresh_token
)
from pydantic import BaseModel, EmailStr, validator
import re
from validate_docbr import CPF, CNPJ

router = APIRouter()

# Tempo de expiração dos tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Função para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📌 Validação de CPF/CNPJ
def validar_cpf_cnpj(value: str):
    value = re.sub(r"\D", "", value)  # Remove caracteres não numéricos
    if len(value) == 11 and CPF().validate(value):
        return value
    elif len(value) == 14 and CNPJ().validate(value):
        return value
    raise ValueError("CPF ou CNPJ inválido")

# 📌 Esquema de entrada para criação do usuário
class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    cpf_cnpj: str
    telefone: str
    tipo_usuario: TipoUsuarioEnum

    # 📌 Validações
    @validator("cpf_cnpj")
    def validar_cpf(cls, v):
        return validar_cpf_cnpj(v)

    @validator("telefone")
    def validar_telefone(cls, v):
        if not re.fullmatch(r"^\d{10,11}$", v):  # Aceita 10 ou 11 dígitos
            raise ValueError("Telefone inválido. Use apenas números (DDD + número)")
        return v

    @validator("senha")
    def validar_senha(cls, v):
        if len(v) < 8 or not re.search(r"\d", v) or not re.search(r"[A-Za-z]", v):
            raise ValueError("A senha deve ter pelo menos 8 caracteres, incluindo letras e números")
        return v

# 📌 Esquema de entrada para login
class UserLogin(BaseModel):
    email: EmailStr
    senha: str

# 📌 Esquema para resposta com tokens
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# 📌 Esquema para Refresh Token
class TokenRefresh(BaseModel):
    refresh_token: str

# 📌 Endpoint para registrar usuário
@router.post("/register", response_model=TokenSchema)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 🔹 Verifica se o e-mail já existe
    if db.query(Usuario).filter(Usuario.email == user.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    # 🔹 Verifica se o CPF/CNPJ já existe
    if db.query(Usuario).filter(Usuario.cpf_cnpj == user.cpf_cnpj).first():
        raise HTTPException(status_code=400, detail="CPF/CNPJ já cadastrado")

    hashed_password = hash_password(user.senha)

    db_user = Usuario(
        nome=user.nome,
        email=user.email,
        senha=hashed_password,
        cpf_cnpj=user.cpf_cnpj,
        telefone=user.telefone,
        tipo_usuario=user.tipo_usuario
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Gera tokens
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(data={"sub": db_user.email})

    # Salva o refresh token no banco
    db_user.refresh_token = refresh_token
    db.commit()

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )

# 🔑 Endpoint para login
@router.post("/login", response_model=TokenSchema)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if not db_user or not verify_password(user.senha, db_user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Gera tokens
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(data={"sub": db_user.email})

    # Atualiza o refresh token no banco
    db_user.refresh_token = refresh_token
    db.commit()

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )

# 🔄 Endpoint para renovar o token de acesso
@router.post("/refresh", response_model=TokenSchema)
def refresh_access_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.refresh_token == token_data.refresh_token).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Refresh Token inválido")

    # Gera novos tokens
    new_access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    new_refresh_token = create_refresh_token(data={"sub": db_user.email})

    # Atualiza o refresh token no banco
    db_user.refresh_token = new_refresh_token
    db.commit()

    return TokenSchema(
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )

# 🚪 Endpoint para logout
@router.post("/logout")
def logout_user(token_data: TokenRefresh, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.refresh_token == token_data.refresh_token).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Refresh Token inválido")

    # Invalida o refresh token
    db_user.refresh_token = None
    db.commit()

    return {"msg": "Logout realizado com sucesso"}
