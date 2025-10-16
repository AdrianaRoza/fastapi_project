from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/")
async def order():
    """
    Essa é uma rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisan de autenticação
    """
    return {"mensagem": "Você acessou a rota de pedidos"}