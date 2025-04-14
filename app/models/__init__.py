# models/__init__.py
from .avaliacao import Avaliacao
from .usuario import Usuario
from .venda import Venda
from .endereco import Endereco
from .cupom import Cupom
from .entrega import Entrega
from .entrega_candidato import EntregaCandidato
from .produto import Produto
from .produto_destaque import ProdutoDestaque
from .produto_imagem import ProdutoImagem
from .estoque import Estoque
from .carrinho import Carrinho
from .item_carrinho import ItemCarrinho  # Adicionei que estava faltando
from .promocao import Promocao
from .itemVenda import ItemVenda
from .pagamento import Pagamento
from .movimentacao_estoque import MovimentacaoEstoque
from .categoria import Categoria
from .categoria_imagem import CategoriaImagem
from .rastreamento_entrega import RastreamentoEntrega
from .entregadorInfo import EntregadorInfo
from .historico_pagamento import HistoricoPagamento
from .listaDesejos import ListaDesejos

__all__ = [
    'Avaliacao',
    'Usuario',
    'Venda',
    'Endereco',
    'Cupom',
    'Entrega',
    'EntregaCandidato',
    'Produto',
    'ProdutoDestaque',
    'ProdutoImagem',
    'Estoque',
    'Carrinho',
    'ItemCarrinho',  # Adicionei
    'Promocao',
    'ItemVenda',
    'Pagamento',
    'MovimentacaoEstoque',
    'Categoria',
    'CategoriaImagem',
    'RastreamentoEntrega',
    'EntregadorInfo',
    'HistoricoPagamento',
    'ListaDesejos'
]