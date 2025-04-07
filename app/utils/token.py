from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings
from app.core.security import SECRET_KEY, ALGORITHM


def criar_token_jwt(dados: dict, tempo_expiracao: int = 60):
    """Gera um token JWT válido por `tempo_expiracao` minutos."""
    dados_copia = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=tempo_expiracao)
    dados_copia.update({"exp": expiracao})
    return jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token_jwt(token: str):
    """Valida e decodifica um token JWT."""
    try:
        dados = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return dados
    except JWTError:
        return None
