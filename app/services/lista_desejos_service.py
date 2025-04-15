from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.models import ListaDesejos
from app.schemas.lista_desejos_schema import ListaDesejosCreate, ListaDesejosResponse
from app.models.produto import Produto
from app.schemas.produto_imagem_schema import ProdutoImagemResponse
from app.schemas.produto_schema import ProdutoResponse


class ListaDesejosService:
    def __init__(self, db: Session):
        self.db = db

    def adicionar_produto(self, usuario_id: int, data: ListaDesejosCreate) -> ListaDesejos:
        # Verifica se o produto já está na lista de desejos
        existente = self.db.query(ListaDesejos).filter_by(
            usuario_id=usuario_id, produto_id=data.produto_id
        ).first()

        if existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Produto já está na lista de desejos"
            )

        # Cria um novo item na lista de desejos
        item = ListaDesejos(usuario_id=usuario_id, produto_id=data.produto_id)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    from sqlalchemy.orm import joinedload

    def listar_desejos_usuario(self, usuario_id: int):
        lista_desejos = (
            self.db.query(ListaDesejos)
            .options(
                joinedload(ListaDesejos.produto).options(
                    joinedload(Produto.imagens),
                    joinedload(Produto.categoria)
                )
            )
            .filter_by(usuario_id=usuario_id)
            .all()
        )

        return [
            ListaDesejosResponse(
                id=desejo.id,
                criado_em=desejo.criado_em.isoformat(),  # Garante conversão para string
                produto=ProdutoResponse.model_validate(desejo.produto)
            )
            for desejo in lista_desejos
        ]

    def remover_produto(self, usuario_id: int, produto_id: int):
        # Verifica se o produto está na lista de desejos
        item = self.db.query(ListaDesejos).filter_by(
            usuario_id=usuario_id, produto_id=produto_id
        ).first()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado na lista de desejos"
            )

        # Remove o item da lista de desejos
        self.db.delete(item)
        self.db.commit()
