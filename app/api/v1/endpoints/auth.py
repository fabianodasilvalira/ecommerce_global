from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.usuario import Usuario, TipoUsuarioEnum
from app.core.security import hash_password, verify_password, create_access_token
from pydantic import BaseModel, EmailStr
from datetime import timedelta

router = APIRouter()

# Esquema para criação do usuário
class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    cpf_cnpj: str
    telefone: str
    tipo_usuario: TipoUsuarioEnum  # Deve ser uma string correspondente ao Enum

# Esquema para login
class UserLogin(BaseModel):
    email: EmailStr
    senha: str

# Função para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint de registro de usuário
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
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
    return {"msg": "Usuário criado com sucesso!"}

# Endpoint de login
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if not db_user or not verify_password(user.senha, db_user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}