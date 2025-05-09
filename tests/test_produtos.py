import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.orm import Session

from app.schemas.produto_schema import ProdutoCreate, ProdutoResponse
from app.models.categoria import Categoria # Para criar categoria de teste

# --- Fixture para criar uma categoria de teste --- (Pode ser movido para conftest.py se usado em múltiplos arquivos)
@pytest.fixture(scope="function")
async def categoria_teste_id(db_session: Session, admin_auth_headers: dict, client: AsyncClient) -> int:
    """Cria uma categoria de teste e retorna seu ID."""
    # Verifica se a categoria já existe para evitar duplicatas em execuções de múltiplos testes
    # Esta é uma simplificação; um setup mais robusto poderia limpar/criar dados de forma mais controlada.
    response_get_cat = await client.get("/api/v1/categorias/?nome=Categoria Teste Produtos", headers=admin_auth_headers)
    if response_get_cat.status_code == status.HTTP_200_OK and response_get_cat.json():
        return response_get_cat.json()[0]["id"]

    categoria_data = {
        "nome": "Categoria Teste Produtos",
        "descricao": "Categoria para testes de produtos",
        "ativo": True
    }
    response = await client.post("/api/v1/categorias/", json=categoria_data, headers=admin_auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]

# --- Testes de Criação de Produto ---
@pytest.mark.asyncio
async def test_criar_novo_produto(client: AsyncClient, admin_auth_headers: dict, categoria_teste_id: int):
    """Testa a criação de um novo produto por um administrador."""
    novo_produto_data = {
        "nome": "Produto Teste 1",
        "descricao": "Descrição do Produto Teste 1",
        "preco": 19.99,
        "categoria_id": categoria_teste_id,
        "volume": 1.5,
        "unidade_medida": "L",
        "ativo": True,
        "margem_lucro": 25.0
    }
    response = await client.post("/api/v1/produtos/", json=novo_produto_data, headers=admin_auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nome"] == novo_produto_data["nome"]
    assert data["preco"] == novo_produto_data["preco"]
    assert data["categoria_id"] == categoria_teste_id
    assert "id" in data
    assert "sku" in data

@pytest.mark.asyncio
async def test_criar_produto_categoria_inexistente(client: AsyncClient, admin_auth_headers: dict):
    """Testa a criação de um produto com uma categoria_id que não existe."""
    produto_data_cat_invalida = {
        "nome": "Produto Categoria Inválida",
        "descricao": "Teste com categoria inexistente",
        "preco": 10.00,
        "categoria_id": 99999, # ID de categoria improvável de existir
        "ativo": True
    }
    response = await client.post("/api/v1/produtos/", json=produto_data_cat_invalida, headers=admin_auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND # Esperado erro de categoria não encontrada
    assert "Categoria com ID 99999 não encontrada" in response.json()["detail"]

# --- Testes de Leitura de Produto ---
@pytest.mark.asyncio
async def test_listar_produtos(client: AsyncClient, admin_auth_headers: dict, categoria_teste_id: int):
    """Testa a listagem de produtos."""
    # Criar alguns produtos para garantir que a lista não esteja vazia
    await client.post("/api/v1/produtos/", json={"nome": "Produto Lista 1", "descricao": "Desc Prod Lista 1", "preco": 5.0, "categoria_id": categoria_teste_id, "ativo": True}, headers=admin_auth_headers)
    await client.post("/api/v1/produtos/", json={"nome": "Produto Lista 2", "descricao": "Desc Prod Lista 2", "preco": 15.0, "categoria_id": categoria_teste_id, "ativo": True}, headers=admin_auth_headers)

    response = await client.get("/api/v1/produtos/", headers=admin_auth_headers) # Admin pode ver todos
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    # A quantidade exata pode variar dependendo de outros testes ou dados preexistentes
    # Vamos verificar se os produtos criados estão na lista
    nomes_na_lista = [prod["nome"] for prod in data]
    assert "Produto Lista 1" in nomes_na_lista
    assert "Produto Lista 2" in nomes_na_lista

@pytest.mark.asyncio
async def test_obter_produto_por_id(client: AsyncClient, admin_auth_headers: dict, categoria_teste_id: int):
    """Testa a obtenção de um produto específico por ID."""
    novo_produto_data = {
        "nome": "Produto Para Buscar ID",
        "descricao": "Descrição do Produto Para Buscar ID",
        "preco": 29.99,
        "categoria_id": categoria_teste_id,
        "ativo": True
    }
    response_create = await client.post("/api/v1/produtos/", json=novo_produto_data, headers=admin_auth_headers)
    assert response_create.status_code == status.HTTP_201_CREATED
    produto_criado_id = response_create.json()["id"]

    response_get = await client.get(f"/api/v1/produtos/{produto_criado_id}", headers=admin_auth_headers)
    assert response_get.status_code == status.HTTP_200_OK
    data = response_get.json()
    assert data["id"] == produto_criado_id
    assert data["nome"] == novo_produto_data["nome"]

@pytest.mark.asyncio
async def test_obter_produto_inexistente(client: AsyncClient, admin_auth_headers: dict):
    """Testa a tentativa de obter um produto com ID inexistente."""
    id_inexistente = 999999
    response = await client.get(f"/api/v1/produtos/{id_inexistente}", headers=admin_auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

# --- Testes de Atualização de Produto ---
@pytest.mark.asyncio
async def test_atualizar_produto(client: AsyncClient, admin_auth_headers: dict, categoria_teste_id: int):
    """Testa a atualização de um produto existente."""
    # Criar produto para atualizar
    produto_original_data = {
        "nome": "Produto Original Para Atualizar",
        "descricao": "Descrição Original",
        "preco": 50.00,
        "categoria_id": categoria_teste_id,
        "ativo": True
    }
    res_create = await client.post("/api/v1/produtos/", json=produto_original_data, headers=admin_auth_headers)
    assert res_create.status_code == status.HTTP_201_CREATED
    produto_id = res_create.json()["id"]

    dados_atualizacao = {"nome": "Produto Nome Atualizado", "preco": 55.50, "descricao": "Descrição Atualizada"}
    response_update = await client.put(f"/api/v1/produtos/{produto_id}", json=dados_atualizacao, headers=admin_auth_headers)
    assert response_update.status_code == status.HTTP_200_OK
    data_atualizado = response_update.json()
    assert data_atualizado["nome"] == "Produto Nome Atualizado"
    assert data_atualizado["preco"] == 55.50
    assert data_atualizado["descricao"] == "Descrição Atualizada"

# --- Testes de Deleção (Inativação) de Produto ---
@pytest.mark.asyncio
async def test_inativar_reativar_produto(client: AsyncClient, admin_auth_headers: dict, categoria_teste_id: int):
    """Testa a inativação e reativação de um produto."""
    produto_data = {
        "nome": "Produto Para Inativar/Reativar",
        "descricao": "Descrição",
        "preco": 10.00,
        "categoria_id": categoria_teste_id,
        "ativo": True
    }
    res_create = await client.post("/api/v1/produtos/", json=produto_data, headers=admin_auth_headers)
    assert res_create.status_code == status.HTTP_201_CREATED
    produto_id = res_create.json()["id"]

    # Inativar
    response_delete = await client.delete(f"/api/v1/produtos/{produto_id}", headers=admin_auth_headers)
    assert response_delete.status_code == status.HTTP_200_OK
    assert response_delete.json()["ativo"] == False

    # Verificar se não lista mais (se a listagem padrão for apenas ativos)
    # response_list = await client.get("/api/v1/produtos/", headers=admin_auth_headers)
    # assert produto_id not in [p["id"] for p in response_list.json() if p["ativo"]]

    # Reativar (o mesmo endpoint DELETE funciona como toggle no serviço)
    response_reactivate = await client.delete(f"/api/v1/produtos/{produto_id}", headers=admin_auth_headers)
    assert response_reactivate.status_code == status.HTTP_200_OK
    assert response_reactivate.json()["ativo"] == True

    # Verificar se está ativo novamente
    res_get = await client.get(f"/api/v1/produtos/{produto_id}", headers=admin_auth_headers)
    assert res_get.status_code == status.HTTP_200_OK
    assert res_get.json()["ativo"] == True

# Adicionar mais testes: validações de campo, SKU único, etc.

