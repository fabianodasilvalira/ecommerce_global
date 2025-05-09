import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.orm import Session
from decimal import Decimal

from app.schemas.venda_schema import VendaCreate, ItemVendaCreate
from app.models.produto import Produto # Para criar produto de teste
from app.models.categoria import Categoria # Para criar categoria de teste
from app.models.endereco import Endereco # Para criar endereço de teste
from app.models.usuario import Usuario # Para obter ID do usuário admin
from app.core.config import settings

# --- Fixture para criar um produto de teste para vendas --- 
@pytest.fixture(scope="function")
async def produto_para_venda_id(db_session: Session, admin_auth_headers: dict, client: AsyncClient, categoria_teste_id: int) -> int:
    """Cria um produto de teste com estoque e retorna seu ID."""
    produto_data = {
        "nome": "Produto Para Venda Teste",
        "descricao": "Descrição do Produto Para Venda",
        "preco": 100.00,
        "categoria_id": categoria_teste_id,
        "ativo": True
    }
    response_prod = await client.post("/api/v1/produtos/", json=produto_data, headers=admin_auth_headers)
    assert response_prod.status_code == status.HTTP_201_CREATED
    produto_id = response_prod.json()["id"]

    # Adicionar estoque ao produto
    estoque_data = {
        "produto_id": produto_id,
        "quantidade": 50,
        "localizacao": "Estoque Principal Teste"
    }
    response_estoque = await client.post(f"/api/v1/estoque/", json=estoque_data, headers=admin_auth_headers)
    assert response_estoque.status_code == status.HTTP_201_CREATED
    return produto_id

# --- Fixture para criar um endereço de teste para o usuário admin ---
@pytest.fixture(scope="function")
async def endereco_admin_id(db_session: Session, admin_auth_headers: dict, client: AsyncClient) -> int:
    """Cria um endereço de teste para o usuário admin e retorna seu ID."""
    # Obter ID do usuário admin (assumindo que o token em admin_auth_headers pertence ao admin)
    # Uma forma mais robusta seria decodificar o token ou ter uma fixture que retorne o objeto do usuário admin
    # Por simplicidade, vamos buscar o admin pelo email.
    admin_user_res = await client.get(f"/api/v1/usuarios/email/{settings.ADMIN_EMAIL}", headers=admin_auth_headers)
    if admin_user_res.status_code != 200:
         # Se não encontrar por email (endpoint pode não existir), cria um usuário e usa o ID dele
        # Este é um fallback, o ideal é ter o ID do admin de forma mais direta
        user_data = {"nome": "Admin Test Address User", "email": "admintestaddress@example.com", "senha": "adminpass", "cpf_cnpj": "00000000000", "tipo_usuario": "admin"}
        res_create_user = await client.post("/api/v1/usuarios/", json=user_data, headers=admin_auth_headers)
        admin_id = res_create_user.json()["id"]
    else:
        admin_id = admin_user_res.json()["id"]

    endereco_data = {
        "usuario_id": admin_id, # Associar ao admin ou a um usuário de teste
        "cep": "12345-678",
        "logradouro": "Rua de Teste para Venda",
        "numero": "123",
        "bairro": "Bairro Teste",
        "cidade": "Cidade Teste",
        "estado": "TS",
        "principal": True
    }
    # Verificar se já existe um endereço principal para o usuário
    # Para simplificar, vamos apenas tentar criar. Se falhar por já existir um principal, o teste pode precisar de ajuste.
    response = await client.post("/api/v1/endereco/", json=endereco_data, headers=admin_auth_headers)
    # Se o endpoint retornar 400 por já existir endereço principal, buscar o existente
    if response.status_code == status.HTTP_400_BAD_REQUEST and "principal já existe" in response.text.lower():
        res_enderecos = await client.get(f"/api/v1/endereco/usuario/{admin_id}", headers=admin_auth_headers)
        enderecos = res_enderecos.json()
        for end in enderecos:
            if end["principal"]:
                return end["id"]
        raise Exception("Não foi possível obter/criar endereço principal para o admin.")
    
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


# --- Testes de Criação de Venda ---
@pytest.mark.asyncio
async def test_criar_nova_venda_simples(client: AsyncClient, admin_auth_headers: dict, produto_para_venda_id: int, endereco_admin_id: int):
    """Testa a criação de uma nova venda simples (um produto, sem cupom, pagamento PIX)."""
    item_venda = ItemVendaCreate(produto_id=produto_para_venda_id, quantidade=2)
    venda_data = VendaCreate(
        endereco_id=endereco_admin_id,
        itens=[item_venda],
        metodo_pagamento="PIX" # Usar string conforme o Enum no schema
    )

    response = await client.post("/api/v1/vendas/", json=venda_data.model_dump(mode='json'), headers=admin_auth_headers)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["status"] == "PENDENTE" # Ou o status inicial definido
    assert len(data["itens"]) == 1
    assert data["itens"][0]["produto_id"] == produto_para_venda_id
    assert data["itens"][0]["quantidade"] == 2
    assert Decimal(str(data["total"])) > Decimal("0.00")
    assert "pagamentos" in data
    assert len(data["pagamentos"]) == 1
    assert data["pagamentos"][0]["metodo_pagamento"] == "PIX"

@pytest.mark.asyncio
async def test_criar_venda_estoque_insuficiente(client: AsyncClient, admin_auth_headers: dict, produto_para_venda_id: int, endereco_admin_id: int):
    """Testa a criação de uma venda com quantidade maior que o estoque disponível."""
    item_venda = ItemVendaCreate(produto_id=produto_para_venda_id, quantidade=1000) # Quantidade muito alta
    venda_data = VendaCreate(
        endereco_id=endereco_admin_id,
        itens=[item_venda],
        metodo_pagamento="BOLETO"
    )

    response = await client.post("/api/v1/vendas/", json=venda_data.model_dump(mode='json'), headers=admin_auth_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Estoque insuficiente" in response.json()["detail"]

# --- Testes de Listagem de Vendas (Simplificado) ---
@pytest.mark.asyncio
async def test_listar_vendas_usuario_logado(client: AsyncClient, admin_auth_headers: dict, produto_para_venda_id: int, endereco_admin_id: int):
    """Testa a listagem de vendas para o usuário logado (admin neste caso)."""
    # Criar uma venda para garantir que haja algo para listar
    item_venda = ItemVendaCreate(produto_id=produto_para_venda_id, quantidade=1)
    venda_data = VendaCreate(endereco_id=endereco_admin_id, itens=[item_venda], metodo_pagamento="DINHEIRO")
    await client.post("/api/v1/vendas/", json=venda_data.model_dump(mode='json'), headers=admin_auth_headers)

    response = await client.get("/api/v1/vendas/", headers=admin_auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0 # Deve haver pelo menos uma venda
    # Verificar se a venda criada (ou uma delas) está na lista
    # Isso pode ser mais complexo se houver muitas vendas; aqui verificamos a estrutura básica
    assert "id" in data[0]
    assert "status" in data[0]
    assert "total" in data[0]
    assert "itens" in data[0]

# Adicionar mais testes: 
# - Venda com cupom
# - Venda com produto em promoção
# - Venda com múltiplos itens
# - Venda com pagamento parcelado (cartão)
# - Cancelamento de venda
# - Detalhamento de venda específica
# - Validações de endereço, etc.

