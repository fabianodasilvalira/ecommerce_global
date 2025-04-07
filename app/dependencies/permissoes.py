from fastapi import Depends, HTTPException, status
from app.models.usuario import TipoUsuarioEnum, Usuario
from app.dependencies.auth import obter_usuario_logado

def permitir_admin(usuario: Usuario = Depends(obter_usuario_logado)):
    if usuario.tipo_usuario != TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para administradores.")
    return usuario

def permitir_funcionario(usuario: Usuario = Depends(obter_usuario_logado)):
    if usuario.tipo_usuario != TipoUsuarioEnum.FUNCIONARIO:
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para funcionários.")
    return usuario

def permitir_admin_ou_funcionario(usuario: Usuario = Depends(obter_usuario_logado)):
    if usuario.tipo_usuario not in [TipoUsuarioEnum.ADMIN, TipoUsuarioEnum.FUNCIONARIO]:
        raise HTTPException(status_code=403, detail="Acesso restrito.")
    return usuario
