from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.v1.endpoints import auth
from app.api.v1.routers.carrinho import router as carrinho_router
from app.api.v1.routers.cartaosalvo import router as cartaosalvo_router
from app.api.v1.routers.categoria import router as categoria_router
from app.api.v1.routers.categoria_imagem import router as categoria_imagem_router
from app.api.v1.routers.cupom import router as cupom_router
from app.api.v1.routers.endereco import router as endereco_router
from app.api.v1.routers.estoque import router as estoque_router
from app.api.v1.routers.historico_pagamento import router as historico_pagamento_router
from app.api.v1.routers.lista_desejos import router as lista_desejos_router
from app.api.v1.routers.movimentacao_estoque import router as movimentacao_estoque_router
from app.api.v1.routers.pagamento import router as pagamento_router
from app.api.v1.routers.produto import router as produto_router
from app.api.v1.routers.produto_destaque import router as produto_destaque_router
from app.api.v1.routers.produto_imagem import router as produto_imagem_router
from app.api.v1.routers.promocao import router as promocao_router
from app.api.v1.routers.relatorios import router as relatorios_router
from app.api.v1.routers.usuario import router as usuario_router
from app.api.v1.routers.venda import router as venda_router
from app.db.database import SessionLocal
from app.services.usuario_service import criar_usuario_admin

app = FastAPI()

from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="E-commerce Global API",
        version="1.0.0",
        description=(
            "API para gerenciamento de um sistema de e-commerce completo.\n\n"
            "### Autenticação:\n"
            "- Esta API é protegida por **JWT (JSON Web Tokens)**.\n"
            "- Para acessar os endpoints protegidos, obtenha um token através do login e utilize o formato `Bearer <seu_token>` no cabeçalho de autorização.\n\n"
            "### Funcionalidades disponíveis:\n"
            "- Gerenciamento de produtos, imagens de produtos e destaques de produtos.\n"
            "- Controle de categorias e imagens de categorias.\n"
            "- Administração de estoques e movimentações de estoque.\n"
            "- Processamento de vendas, itens de venda e histórico de pagamentos.\n"
            "- Gestão de usuários, endereços e métodos de pagamento.\n"
            "- Funcionalidades de carrinho de compras e itens do carrinho.\n"
            "- Gerenciamento de cupons de desconto e promoções.\n"
            "- Lista de desejos dos usuários.\n"
            "- Avaliações de produtos.\n"
            "- Relatórios administrativos.\n"
            "- Rastreamento de entregas e gestão de entregadores candidatos."
        ),

        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Insira o token JWT no formato **Bearer &lt;seu_token&gt;**",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    criar_usuario_admin(db)  # Chama a função para criar o admin
    db.close()

# Inclusão de rotas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(carrinho_router, prefix="/api/v1/carrinho", tags=["carrinho"])
app.include_router(cartaosalvo_router, prefix="/api/v1/cartaosalvo", tags=["cartaosalvo"])
app.include_router(categoria_router, prefix="/api/v1/categorias", tags=["categorias"])
app.include_router(categoria_imagem_router, prefix="/api/v1/categoria_imagem", tags=["categoria_imagem"])
app.include_router(cupom_router, prefix="/api/v1/cupons", tags=["cupons"])
app.include_router(endereco_router, prefix="/api/v1/endereco", tags=["endereco"])
app.include_router(estoque_router, prefix="/api/v1/estoque", tags=["estoque"])
app.include_router(historico_pagamento_router, prefix="/api/v1/historico_pagamento", tags=["historico_pagamento"])
app.include_router(lista_desejos_router, prefix="/api/v1/lista_desejos", tags=["lista_desejos"])
app.include_router(movimentacao_estoque_router, prefix="/api/v1/movimentacao_estoque", tags=["movimentacao_estoque"])
app.include_router(pagamento_router, prefix="/api/v1/pagamento", tags=["pagamento"])
app.include_router(produto_destaque_router, prefix="/api/v1/produto_destaque", tags=["produto_destaque"])
app.include_router(produto_imagem_router, prefix="/api/v1/produto_imagem", tags=["produto_imagem"])
app.include_router(produto_router, prefix="/api/v1/produtos", tags=["produtos"])
app.include_router(promocao_router, prefix="/api/v1/promocao", tags=["promocao"])
app.include_router(relatorios_router, prefix="/api/v1/relatorios", tags=["relatorios"])
app.include_router(usuario_router, prefix="/api/v1/usuarios", tags=["usuários"])
app.include_router(venda_router, prefix="/api/v1/vendas", tags=["vendas"])

