import pytest
from httpx import AsyncClient
from fastapi import status

from app.main import app # Importar a instância da aplicação FastAPI
from app.core.config import settings # Para pegar credenciais do admin se necessário

# Usar um cliente assíncrono para testes com FastAPI
@pytest.mark.asyncio
async def test_login_admin_success(client: AsyncClient):
    """Testa o login bem-sucedido do usuário administrador padrão."""
    # As credenciais do admin são carregadas de variáveis de ambiente em usuario_service.py
    # Para o teste, podemos usar as mesmas variáveis ou mocká-las se necessário.
    # Vamos assumir que o usuário admin é criado no startup do app.
    login_data = {
        "username": settings.ADMIN_EMAIL, # Usar o email do admin configurado
        "password": settings.ADMIN_PASSWORD # Usar a senha do admin configurada
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert response_data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Testa o login com credenciais inválidas."""
    login_data = {
        "username": "usuarioinexistente@example.com",
        "password": "senhainvalida123"
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response_data = response.json()
    assert response_data["detail"] == "Credenciais inválidas"

# Adicionar um fixture para o cliente HTTP assíncrono, se ainda não existir em um conftest.py
# Por enquanto, vamos assumir que o client é passado externamente ou será configurado depois.
# Se for necessário um conftest.py, ele seria criado assim:
# tests/conftest.py
# import pytest
# from httpx import AsyncClient
# from app.main import app
# 
# @pytest.fixture(scope="session")
# async def client():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         yield ac

