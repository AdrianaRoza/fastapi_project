from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import capture_session, verify_token
from schemas import OrderSchemas
from models import Order, User

order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verify_token)])

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

@order_router.post("/order/cancelled/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(capture_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    order.status = "CANCELADO"
    session.commit()
    return{
        "mensage": f"Pedido de número: {order_id} cancelado com sucesso",
        "order":order
}


@order_router.get("/list")
async def list_order(session: Session = Depends(capture_session), user: User = Depends(verify_token)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    else: 
        order = session.query(Order).all()
        return{
            "order": order
        }