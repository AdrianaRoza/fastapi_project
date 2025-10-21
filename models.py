from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType


# cria a conexão do seu banco
db = create_engine("sqlite:///banco.db")

#cria a base do banco de dados
Base = declarative_base()

#cria as classes/tabelas do banco
class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email",String, nullable=False)
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin



#Pedidos
class order(Base):
    __tablename__= "orders"

    STATUS_PEDIDOS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO")
    )

    id = Column("id",Integer,primary_key=True, autoincrement=True)
    status = Column("status",ChoiceType(choices=STATUS_PEDIDOS)) #pendentre, cancelado, finalizado
    user = Column("user",ForeignKey("users.id"))
    price = Column("price", Float)
   # itens =


    def __init__(self, user,status="PENDENTE",price=0):
        self.user = user
        self.price = price
        self.status = status


#Itens do pedido

class orderedItem(Base):
    __tablename__ = "orderedItems"

    id = Column("id",Integer,primary_key=True, autoincrement=True)
    amount = Column("amount", Integer)
    flavor = Column("flavor", String)
    size = Column("size",String)
    unit_price = Column("unit_price", Float)
    order = Column("order", ForeignKey("orders.id"))


    def __init__( self, amount, flavor, size, unit_price, order):
        self.amount = amount
        self.flavor = flavor
        self.size = size
        self.unit_price = unit_price
        self.order = order
    

#executa a criação dos metadados do se banco (cria efetivamente o banco de dados)