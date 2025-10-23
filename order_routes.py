from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import capture_session
from schemas import OrderSchemas
from models import Order

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/")
async def order():
    """
    Essa é uma rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisan de autenticação
    """
    return {"mensagem": "Você acessou a rota de pedidos"}

@order_router.post("/order")
async def create_order(order_schemas: OrderSchemas, session: Session = Depends(capture_session)):
    new_order = Order(user=order_schemas.user)
    session.add(new_order)
    session.commit()
    return{"mensagem": f"Pedido criado com sucesso. ID do pedido:{new_order.id}"}