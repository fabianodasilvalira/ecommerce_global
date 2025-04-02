from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.utils.security import verificar_senha
from app.utils.token import criar_token_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def autenticar_usuario(email: str, senha: str, db: Session):
    """Verifica credenciais e retorna o usuário autenticado"""
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not verificar_senha(senha, usuario.senha):
        return None
    return usuario

def obter_usuario_logado(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Obtém o usuário logado através do token"""
    dados_token = verificar_token_jwt(token)
    if not dados_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    usuario = db.query(Usuario).filter(Usuario.id == dados_token["sub"]).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    return usuario
