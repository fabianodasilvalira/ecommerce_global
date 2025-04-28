from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.endereco import EnderecoCreate, EnderecoUpdate, EnderecoOut
from app.services import endereco_service
from app.core.security import get_current_user  # Função de autenticação

router = APIRouter()


# 🧾 Criar novo endereço
@router.post(
    "/",
    response_model=EnderecoOut,
    summary="Criar novo endereço",
    status_code=status.HTTP_201_CREATED,
    response_description="Endereço criado com sucesso"
)
def criar(
        endereco: EnderecoCreate,
        db: Session = Depends(get_db),
        usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Cria um novo endereço no sistema.

    **Parâmetros**:
        - **endereco**: Dados do endereço a ser criado.

    **Respostas**:
        - **201 Created**: Endereço criado com sucesso.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    return endereco_service.criar_endereco(db, endereco)


# 📜 Listar endereços (por ID de usuário opcional)
@router.get(
    "/",
    response_model=list[EnderecoOut],
    summary="Listar endereços",
    response_description="Lista de endereços"
)
def listar(
        usuario_id: int = None,
        db: Session = Depends(get_db),
        usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Lista todos os endereços de um usuário, se fornecido o `usuario_id`.

    **Parâmetros**:
        - **usuario_id**: ID do usuário cujos endereços serão listados. (Opcional)

    **Respostas**:
        - **200 OK**: Retorna a lista de endereços.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    return endereco_service.listar_enderecos(db, usuario_id)


# 🔍 Buscar endereço por ID
@router.get(
    "/{endereco_id}",
    response_model=EnderecoOut,
    summary="Buscar endereço por ID",
    response_description="Detalhes do endereço encontrado"
)
def buscar(
        endereco_id: int,
        db: Session = Depends(get_db),
        usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Busca um endereço específico baseado no ID fornecido.

    **Parâmetros**:
        - **endereco_id**: ID do endereço a ser buscado.

    **Respostas**:
        - **200 OK**: Retorna os detalhes do endereço.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
        - **404 Not Found**: Se o endereço com o ID fornecido não for encontrado.
    """
    endereco = endereco_service.buscar_endereco(db, endereco_id)
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return endereco


# ✏️ Atualizar endereço por ID
@router.put(
    "/{endereco_id}/editar",
    response_model=EnderecoOut,
    summary="Editar endereço",
    response_description="Endereço atualizado com sucesso"
)
def atualizar(
        endereco_id: int,
        dados: EnderecoUpdate,
        db: Session = Depends(get_db),
        usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Atualiza os dados de um endereço específico.

    **Parâmetros**:
        - **endereco_id**: ID do endereço a ser atualizado.
        - **dados**: Dados atualizados do endereço.

    **Respostas**:
        - **200 OK**: Endereço atualizado com sucesso.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
        - **404 Not Found**: Se o endereço com o ID fornecido não for encontrado.
    """
    endereco = endereco_service.atualizar_endereco(db, endereco_id, dados)
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return endereco


# 🗑️ Inativar endereço por ID
@router.delete(
    "/{endereco_id}/inativar",
    summary="Inativar endereço",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Endereço inativado com sucesso"
)
def inativar(
        endereco_id: int,
        db: Session = Depends(get_db),
        usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Inativa um endereço específico.

    **Parâmetros**:
        - **endereco_id**: ID do endereço a ser inativado.

    **Respostas**:
        - **204 No Content**: Endereço inativado com sucesso.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
        - **404 Not Found**: Se o endereço com o ID fornecido não for encontrado ou já estiver inativado.
    """
    endereco = endereco_service.inativar_endereco(db, endereco_id)
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado ou já inativado")
    return {"ok": True, "msg": "Endereço inativado com sucesso"}
