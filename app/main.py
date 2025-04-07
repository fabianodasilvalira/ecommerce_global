from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.staticfiles import StaticFiles

from app.api.v1.endpoints import auth
from app.api.v1.routers.produto import router as produto_router
from app.api.v1.routers.produto_imagem import router as produto_imagem_router
from app.api.v1.routers.categoria import router as categoria_router
from app.api.v1.routers.estoque import router as estoque_router
from app.api.v1.routers.cupom import router as cupom_router
from app.api.v1.routers.promocao import router as promocao_router
from app.api.v1.routers.endereco import router as endereco_router
from app.api.v1.routers.produto_destaque import router as produto_destaque_router
from app.api.v1.routers.usuario import router as usuario_router
from app.api.v1.routers.historico_pagamento import router as historico_pagamento_router
from app.api.v1.routers.relatorios import router as relatorios_router

app = FastAPI()

from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sua API",
        version="1.0.0",
        description="Documentação protegida com JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Ativando o schema customizado
app.openapi = custom_openapi


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(produto_router, prefix="/api/v1", tags=["produtos"])
app.include_router(produto_imagem_router, prefix="/api/v1", tags=["produto_imagem"])
app.include_router(produto_destaque_router, prefix="/api/v1", tags=["produto_destaque"])
app.include_router(categoria_router, prefix="/api/v1", tags=["categorias"])
app.include_router(estoque_router, prefix="/api/v1", tags=["estoque"])
app.include_router(cupom_router, prefix="/api/v1", tags=["cupons"])
app.include_router(promocao_router, prefix="/api/v1", tags=["promocao"])
app.include_router(endereco_router, prefix="/api/v1", tags=["endereco"])
app.include_router(usuario_router, prefix="/api/v1/usuarios", tags=["usuários"])
app.include_router(historico_pagamento_router, prefix="/api/v1", tags=["historico_pagamento"])
app.include_router(relatorios_router, prefix="/api/v1", tags=["relatorios"])

