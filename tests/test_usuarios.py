import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.orm import Session

from app.schemas.usuario_schema import UsuarioCreate, UsuarioOut
from app.services.usuario_service import get_password_hash # Para criar senha mock
from app.core.config import settings

# --- Testes de Criação de Usuário ---
@pytest.mark.asyncio
async def test_criar_novo_usuario_como_admin(client: AsyncClient, admin_auth_headers: dict):
    """Testa a criação de um novo usuário (não admin) por um administrador."""
    novo_usuario_data = {
        "nome": "Usuário Teste Criado Por Admin",
        "email": "usuariotestecriado@example.com",
        "senha": "senhaforte123",
        "cpf_cnpj": "12345678902",
        "telefone": "11987654321",
        "tipo_usuario": "cliente" # Admin pode definir o tipo
    }
    response = await client.post("/api/v1/usuarios/", json=novo_usuario_data, headers=admin_auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == novo_usuario_data["email"]
    assert data["nome"] == novo_usuario_data["nome"]
    assert "id" in data
    # Não deve retornar a senha
    assert "senha" not in data

@pytest.mark.asyncio
async def test_criar_usuario_email_duplicado(client: AsyncClient, admin_auth_headers: dict):
    """Testa a tentativa de criar um usuário com e-mail já existente."""
    # Primeiro, cria um usuário
    usuario_existente_data = {
        "nome": "Usuário Email Duplicado",
        "email": "emailduplicado@example.com",
        "senha": "senha123",
        "cpf_cnpj": "00011122233",
        "tipo_usuario": "cliente"
    }
    response_primeiro = await client.post("/api/v1/usuarios/", json=usuario_existente_data, headers=admin_auth_headers)
    assert response_primeiro.status_code == status.HTTP_201_CREATED

    # Tenta criar outro com o mesmo email
    response_segundo = await client.post("/api/v1/usuarios/", json=usuario_existente_data, headers=admin_auth_headers)
    assert response_segundo.status_code == status.HTTP_400_BAD_REQUEST # Esperado erro de duplicação
    # A mensagem de erro pode variar dependendo da implementação do serviço
    # assert "Email já cadastrado" in response_segundo.json()["detail"]

# --- Testes de Leitura de Usuário ---
@pytest.mark.asyncio
async def test_listar_usuarios_como_admin(client: AsyncClient, admin_auth_headers: dict):
    """Testa a listagem de usuários por um administrador."""
    # Criar alguns usuários para garantir que a lista não esteja vazia
    await client.post("/api/v1/usuarios/", json={"nome": "User List Test 1", "email": "userlist1@example.com", "senha": "pass1", "cpf_cnpj": "11100011100", "tipo_usuario": "cliente"}, headers=admin_auth_headers)
    await client.post("/api/v1/usuarios/", json={"nome": "User List Test 2", "email": "userlist2@example.com", "senha": "pass2", "cpf_cnpj": "22200022200", "tipo_usuario": "fornecedor"}, headers=admin_auth_headers)
    
    response = await client.get("/api/v1/usuarios/", headers=admin_auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2 # Pelo menos os dois criados mais o admin
    # Verificar se os emails dos usuários criados estão na lista
    emails_na_lista = [user["email"] for user in data]
    assert "userlist1@example.com" in emails_na_lista
    assert "userlist2@example.com" in emails_na_lista
    assert settings.ADMIN_EMAIL in emails_na_lista # Admin também deve estar listado

@pytest.mark.asyncio
async def test_obter_usuario_por_id_como_admin(client: AsyncClient, admin_auth_headers: dict):
    """Testa a obtenção de um usuário específico por ID por um administrador."""
    # Criar um usuário para buscar
    novo_usuario_data = {
        "nome": "Usuário Para Buscar",
        "email": "buscarporid@example.com",
        "senha": "senhaforte123",
        "cpf_cnpj": "98765432100",
        "tipo_usuario": "cliente"
    }
    response_create = await client.post("/api/v1/usuarios/", json=novo_usuario_data, headers=admin_auth_headers)
    assert response_create.status_code == status.HTTP_201_CREATED
    usuario_criado_id = response_create.json()["id"]

    response_get = await client.get(f"/api/v1/usuarios/{usuario_criado_id}", headers=admin_auth_headers)
    assert response_get.status_code == status.HTTP_200_OK
    data = response_get.json()
    assert data["id"] == usuario_criado_id
    assert data["email"] == novo_usuario_data["email"]

@pytest.mark.asyncio
async def test_obter_usuario_inexistente(client: AsyncClient, admin_auth_headers: dict):
    """Testa a tentativa de obter um usuário com ID inexistente."""
    id_inexistente = 999999
    response = await client.get(f"/api/v1/usuarios/{id_inexistente}", headers=admin_auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

# --- Testes de Atualização de Usuário ---
@pytest.mark.asyncio
async def test_atualizar_proprio_usuario(client: AsyncClient, db_session: Session):
    """Testa se um usuário comum pode atualizar seus próprios dados (exceto tipo_usuario e ativo)."""
    # 1. Criar um usuário comum (sem ser admin) para o teste
    #    Idealmente, teríamos um endpoint de registro público ou criaríamos diretamente no DB para teste.
    #    Por simplicidade, vamos criar via admin e depois logar como esse usuário.
    admin_headers = await admin_auth_headers(client) # Obtem headers do admin
    
    usuario_comum_data_create = {
        "nome": "Usuário Comum Para Atualizar",
        "email": "comumupdate@example.com",
        "senha": "comumsenha123",
        "cpf_cnpj": "10101010101",
        "tipo_usuario": "cliente"
    }
    res_create = await client.post("/api/v1/usuarios/", json=usuario_comum_data_create, headers=admin_headers)
    assert res_create.status_code == status.HTTP_201_CREATED
    usuario_comum_id = res_create.json()["id"]

    # 2. Logar como o usuário comum criado
    login_comum_data = {"username": "comumupdate@example.com", "password": "comumsenha123"}
    res_login_comum = await client.post("/auth/login", data=login_comum_data)
    assert res_login_comum.status_code == status.HTTP_200_OK
    token_comum = res_login_comum.json()["access_token"]
    headers_comum = {"Authorization": f"Bearer {token_comum}"}

    # 3. Tentar atualizar os dados do próprio usuário
    dados_atualizacao = {"nome": "Nome Comum Atualizado", "telefone": "22987654321"}
    response_update = await client.put(f"/api/v1/usuarios/{usuario_comum_id}", json=dados_atualizacao, headers=headers_comum)
    assert response_update.status_code == status.HTTP_200_OK
    data_atualizado = response_update.json()
    assert data_atualizado["nome"] == "Nome Comum Atualizado"
    assert data_atualizado["telefone"] == "22987654321"

@pytest.mark.asyncio
async def test_admin_atualiza_outro_usuario(client: AsyncClient, admin_auth_headers: dict):
    """Testa se um admin pode atualizar dados de outro usuário, incluindo tipo e status ativo."""
    # Criar um usuário para ser atualizado pelo admin
    usuario_alvo_data = {
        "nome": "Usuário Alvo do Admin",
        "email": "alvoadmin@example.com",
        "senha": "alvosenha",
        "cpf_cnpj": "30303030303",
        "tipo_usuario": "cliente"
    }
    res_create = await client.post("/api/v1/usuarios/", json=usuario_alvo_data, headers=admin_auth_headers)
    assert res_create.status_code == status.HTTP_201_CREATED
    usuario_alvo_id = res_create.json()["id"]

    dados_atualizacao_admin = {
        "nome": "Nome Alvo Atualizado Pelo Admin",
        "tipo_usuario": "fornecedor",
        "ativo": False
    }
    response_update = await client.put(f"/api/v1/usuarios/{usuario_alvo_id}", json=dados_atualizacao_admin, headers=admin_auth_headers)
    assert response_update.status_code == status.HTTP_200_OK
    data_atualizado = response_update.json()
    assert data_atualizado["nome"] == "Nome Alvo Atualizado Pelo Admin"
    assert data_atualizado["tipo_usuario"] == "fornecedor"
    assert data_atualizado["ativo"] == False

# --- Testes de Deleção (Inativação) de Usuário ---
@pytest.mark.asyncio
async def test_admin_inativa_usuario(client: AsyncClient, admin_auth_headers: dict):
    """Testa se um admin pode inativar (soft delete) um usuário."""
    # Criar um usuário para ser inativado
    usuario_para_inativar_data = {
        "nome": "Usuário Para Inativar",
        "email": "inativar@example.com",
        "senha": "senha123",
        "cpf_cnpj": "40404040404",
        "tipo_usuario": "cliente"
    }
    res_create = await client.post("/api/v1/usuarios/", json=usuario_para_inativar_data, headers=admin_auth_headers)
    assert res_create.status_code == status.HTTP_201_CREATED
    usuario_para_inativar_id = res_create.json()["id"]

    response_delete = await client.delete(f"/api/v1/usuarios/{usuario_para_inativar_id}", headers=admin_auth_headers)
    assert response_delete.status_code == status.HTTP_200_OK # ou 204 se não retornar conteúdo
    data_inativado = response_delete.json()
    assert data_inativado["ativo"] == False

    # Tentar buscar o usuário inativado (geralmente não deve aparecer em listagens padrão)
    # Ou verificar diretamente no banco se o status 'ativo' é False.
    # Para este teste, vamos assumir que o endpoint de GET por ID ainda retorna o usuário, mas com ativo=False.
    res_get_inativado = await client.get(f"/api/v1/usuarios/{usuario_para_inativar_id}", headers=admin_auth_headers)
    assert res_get_inativado.status_code == status.HTTP_200_OK # ou 404 se o GET não retornar inativos
    assert res_get_inativado.json()["ativo"] == False

# Adicionar mais testes conforme necessário: permissões, validações de campo, etc.

