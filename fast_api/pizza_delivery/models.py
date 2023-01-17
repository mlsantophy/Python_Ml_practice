from models.database import Base
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey
from sqlalchemy_utils.types import ChoiceType                    #for choice
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True)
    username=Column(String(25),unique=True)
    email=Column(String(55),unique=True)
    password=Column(Text,nullable=True)
    is_staff=Column(Boolean,default=False)
    is_active=Column(Boolean,default=False)
    orders=relationship('Order',back_populates='user')


    def __repr__(self):
        return f"<User {self.username}>"


class Order(Base):
    
    ORDER_STATUS=(
        ('PENDING','pending'),
        ('IN_TRANSIT','in-transit'),
        ('DELIVERED','delivered')
    )

    PIZZA_SIZE=(
        ('SMALL','small'),
        ('MEDIUM','medium'),
        ('LARGE','large'),
        ('EXTRA-LARGE','extra-large')
    )
    


    
    __tablename__="orders"
    id=Column(Integer,primary_key=True)
    quantity=Column(Integer,nullable=False)
    order_status=Column(ChoiceType(choices=ORDER_STATUS),default="PENDING")
    pizza_size=Column(ChoiceType(choices=PIZZA_SIZE),default='MEDIUM')
    user_id=Column(Integer,ForeignKey('user.id'))
    user=relationship('User',back_populates='order')


    def __repr__(self):
        return f"<Order {self.id}>"




