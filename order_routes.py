from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import capture_session, verify_token
from schemas import OrderSchemas, ItemOrderSchema, ResponseOrderSchema
from models import Order, User, OrderedItem
from typing import List

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

@order_router.post("/order/cancelled/{id_order}")
async def cancel_order(id_order: int, session: Session = Depends(capture_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==id_order).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    order.status = "CANCELADO"
    session.commit()
    return{
        "mensage": f"Pedido de número: {order.id} cancelado com sucesso",
        "order": order
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
    


@order_router.post("/order/add-item/{id_order}")
async def add_item_order(id_order: int,
                         item_order_schema: ItemOrderSchema, 
                         session: Session = Depends(capture_session), 
                         user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==id_order).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido não existente")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="Você não tem autorização para essa operação")
    item_order = OrderedItem(item_order_schema.amount,
                             item_order_schema.flavor,
                             item_order_schema.size,
                             item_order_schema.unit_price,
                             id_order)
    session.add(item_order)
    order.calculate_price()
    session.commit()
    return{
        "mensage": "Item criado com sucesso",
        "item_id": item_order.id,
        "preco_pedido": order.price
    }


@order_router.post("/order/remove-item/{id_item_order}")
async def remove_item_order(id_item_order: int, 
                         session: Session = Depends(capture_session), 
                         user: User = Depends(verify_token)):
    item_order = session.query(OrderedItem).filter(OrderedItem.id==id_item_order).first()
    if not item_order:
        raise HTTPException(status_code=404, detail=f"Item {id_item_order} não encontrado")
    order = session.query(Order).filter(Order.id==item_order.order).first()
    if not item_order:
        raise HTTPException(status_code=400, detail="Item no pedido não existente")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="Você não tem autorização para essa operação")
    session.delete(item_order)
    order.calculate_price()
    session.commit()
    return{
        "mensage": "Item removido com sucesso",
        "amount_itens_order": len(order.itens),
        "order": order
    }



@order_router.post("/order/finish/{id_order}")
async def finish_order(id_order: int, session: Session = Depends(capture_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==id_order).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    order.status = "FINALIZADO"
    session.commit()
    return{
        "mensage": f"Pedido de número: {order.id} finalizado com sucesso",
        "order": order
}


@order_router.get("/pedido/{id_order}")
async def view_order(id_order: int, session: Session = Depends(capture_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==id_order).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    return{
        "amount_itens_order": len(order.itens),
        "order": order
    }


@order_router.get("/list/order-user", response_model=List[ResponseOrderSchema])
async def list_order(session: Session = Depends(capture_session), user: User = Depends(verify_token)): 
        order = session.query(Order).filter(Order.user==user.id).all()
        return order