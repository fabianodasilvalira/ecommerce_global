from .usuario import Usuario
from .venda import Venda
from .endereco import Endereco
from .cupom import Cupom
from .entrega import Entrega  # Adicione esta linha
from .produto import Produto
from .produto_imagem import ProdutoImagem
from .estoque import Estoque  # Adicione esta linha
from .avaliacao import Avaliacao  # Adicione esta linha
from .promocao import Promocao
from .itemVenda import ItemVenda           # Adicione esta linha

from .categoria import Categoria
# ... outros imports
# ... outros modelos

__all__ = ['Produto', 'ProdutoImagem', 'Estoque', 'Avaliacao', 'Categoria', 'Usuario', 'Promocao', 'ItemVenda', ...]
