from sqlalchemy.orm import Session
from app.models.cartaoSalvo import CartaoSalvo
from app.schemas.cartaosalvo_schema import CartaoSalvoCreate

def criar_cartao_salvo(db: Session, usuario_id: int, cartao_data: CartaoSalvoCreate):
    novo_cartao = CartaoSalvo(
        usuario_id=usuario_id,
        bandeira=cartao_data.bandeira,
        ultimos_digitos=cartao_data.ultimos_digitos,
        nome_impresso=cartao_data.nome_impresso,
        token_cartao=cartao_data.token_cartao
    )
    db.add(novo_cartao)
    db.commit()
    db.refresh(novo_cartao)
    return novo_cartao

def listar_cartoes_usuario(db: Session, usuario_id: int):
    return db.query(CartaoSalvo).filter(CartaoSalvo.usuario_id == usuario_id).all()

def deletar_cartao_salvo(db: Session, cartao_id: int, usuario_id: int):
    cartao = db.query(CartaoSalvo).filter(
        CartaoSalvo.id == cartao_id,
        CartaoSalvo.usuario_id == usuario_id
    ).first()
    if cartao:
        db.delete(cartao)
        db.commit()
        return True
    return False
