from fastapi import FastAPI

from app.api.v1.endpoints import auth
from app.api.v1.routers.produto import router as produto_router  # Rota de produto
from app.api.v1.routers.categoria import router as categoria_router  # Rota de categoria

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(produto_router, prefix="/api/v1", tags=["produtos"])
app.include_router(categoria_router, prefix="/api/v1", tags=["categorias"])

