from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.usuario import TipoUsuarioEnum, Usuario
from app.services.auth import obter_usuario_logado


def permissao_necessaria(*tipos: TipoUsuarioEnum):
    def wrapper(usuario: Usuario = Depends(obter_usuario_logado)):
        if usuario.tipo_usuario not in tipos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão negada para este tipo de usuário"
            )
        return usuario
    return wrapper
