from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import autenticar_usuario
from app.db.database import get_db
from app.core.security import gerar_tokens  # certifique-se de importar

router = APIRouter()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Realiza o login do usuário autenticando suas credenciais (usuário e senha) e gera os tokens de acesso.

    Parâmetros:
    - **form_data**: Contém as credenciais do usuário, como nome de usuário e senha, fornecidas no corpo da requisição.
    - **db**: Sessão do banco de dados para validação do usuário.

    Retorno:
    - **tokens**: Retorna os tokens de acesso (access token e refresh token) se as credenciais forem válidas.

    Exceções:
    - **HTTPException**: Caso as credenciais sejam inválidas, um erro 401 será retornado com a mensagem "Credenciais inválidas".
    """
    usuario = autenticar_usuario(form_data.username, form_data.password, db)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return gerar_tokens(usuario.id)
