from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import autenticar_usuario
from app.db.database import get_db
from app.core.security import gerar_tokens  # certifique-se de importar

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = autenticar_usuario(form_data.username, form_data.password, db)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return gerar_tokens(usuario.id)