import logging
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from app.models import ProdutoDestaque, Produto
from app.schemas.produto_destaque_schema import (
    ProdutoDestaqueCreate,
    ProdutoDestaqueUpdate,
    TipoDestaqueEnum
)
import psycopg2
from psycopg2 import errors

logger = logging.getLogger(__name__)


class ProdutoDestaqueService:
    def __init__(self, db: Session):
        self.db = db

    def verificar_existencia(self, destaque_id: int) -> ProdutoDestaque:
        """Verifica se o destaque existe e retorna o objeto ou levanta exceção"""
        db_destaque = self.obter_destaque_por_id(destaque_id)
        if not db_destaque:
            logger.warning(f"Destaque com ID {destaque_id} não encontrado.")
            raise HTTPException(
                status_code=404,
                detail=f"Destaque com ID {destaque_id} não encontrado."
            )
        return db_destaque

    def verificar_produto_existente(self, produto_id: int) -> None:
        """Verifica se o produto existe ou levanta exceção"""
        db_produto = self.db.query(Produto).filter(Produto.id == produto_id).first()
        if not db_produto:
            logger.warning(f"Produto com ID {produto_id} não encontrado.")
            raise HTTPException(
                status_code=404,
                detail=f"Produto com ID {produto_id} não encontrado."
            )

    def criar_destaque(self, destaque: ProdutoDestaqueCreate) -> ProdutoDestaque:
        """
        Cria um novo destaque para um produto
        """
        self.verificar_produto_existente(destaque.produto_id)

        db_destaque = ProdutoDestaque(
            produto_id=destaque.produto_id,
            posicao=destaque.posicao,
            tipo_destaque=destaque.tipo_destaque.value
        )

        try:
            self.db.add(db_destaque)
            self.db.commit()
            self.db.refresh(db_destaque)
            logger.info(f"Destaque criado com sucesso para o produto ID {destaque.produto_id}")
            return db_destaque
        except IntegrityError as e:
            self.db.rollback()
            if isinstance(e.orig, psycopg2.errors.ForeignKeyViolation):
                logger.error(f"Erro ao criar destaque: Produto com ID {destaque.produto_id} não encontrado.")
                raise HTTPException(
                    status_code=404,
                    detail=f"Produto com ID {destaque.produto_id} não encontrado."
                )
            elif isinstance(e.orig, psycopg2.errors.UniqueViolation):
                logger.error(f"Destaque já existe para o produto com ID {destaque.produto_id}.")
                raise HTTPException(
                    status_code=400,
                    detail="Destaque já existe para esse produto."
                )
            logger.error(f"Erro desconhecido ao criar destaque: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail="Erro ao criar destaque."
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro interno ao criar destaque: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro interno: {str(e)}"
            )

    def listar_destaques(
            self,
            tipo: Optional[TipoDestaqueEnum] = None,
            ativo: Optional[bool] = True
    ) -> List[ProdutoDestaque]:
        """
        Lista os destaques com filtros opcionais por tipo e status
        """
        query = self.db.query(ProdutoDestaque)

        if tipo:
            query = query.filter(ProdutoDestaque.tipo_destaque == tipo.value)

        if ativo is not None:
            query = query.filter(ProdutoDestaque.ativo == ativo)

        return query.order_by(ProdutoDestaque.posicao).all()

    def obter_destaque_por_id(self, destaque_id: int) -> Optional[ProdutoDestaque]:
        """Obtém um destaque pelo ID ou retorna None"""
        return self.db.query(ProdutoDestaque).filter(ProdutoDestaque.id == destaque_id).first()

    def atualizar_destaque(
            self,
            destaque_id: int,
            destaque: ProdutoDestaqueUpdate
    ) -> ProdutoDestaque:
        """
        Atualiza os dados de um destaque existente
        """
        db_destaque = self.verificar_existencia(destaque_id)
        update_data = destaque.model_dump(exclude_unset=True)

        # Converte enum para string se necessário
        if 'tipo_destaque' in update_data and update_data['tipo_destaque'] is not None:
            update_data['tipo_destaque'] = update_data['tipo_destaque'].value

        for key, value in update_data.items():
            setattr(db_destaque, key, value)

        try:
            self.db.commit()
            self.db.refresh(db_destaque)
            return db_destaque
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao atualizar destaque: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao atualizar destaque: {str(e)}"
            )

    def remover_destaque(self, destaque_id: int) -> ProdutoDestaque:
        """
        Remove um destaque pelo ID
        """
        db_destaque = self.verificar_existencia(destaque_id)
        try:
            self.db.delete(db_destaque)
            self.db.commit()
            logger.info(f"Destaque com ID {destaque_id} removido com sucesso.")
            return db_destaque
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao remover destaque: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao remover destaque: {str(e)}"
            )

    def alternar_status_destaque(self, destaque_id: int) -> ProdutoDestaque:
        """
        Alterna o status ativo/inativo de um destaque
        """
        db_destaque = self.verificar_existencia(destaque_id)
        db_destaque.ativo = not db_destaque.ativo

        try:
            self.db.commit()
            self.db.refresh(db_destaque)
            logger.info(
                f"Status do destaque com ID {destaque_id} alterado para "
                f"{'ativo' if db_destaque.ativo else 'inativo'}."
            )
            return db_destaque
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao alternar status do destaque: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao alternar status do destaque: {str(e)}"
            )