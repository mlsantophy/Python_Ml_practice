from fastapi import APIRouter,Depends,HTTPException,status
from fastapi_jwt_auth import AuthJWT
from mode.models import User,Order
from schemas import OrderModel,OrderStatusModel
from mode.database import Session,engine
from fastapi.encoders import jsonable_encoder


router=APIRouter(
    prefix="/orders",
    tags=['orders']
)

session=Session(bind=engine)

@router.get('/')
def hello(Authorize:AuthJWT=Depends()):

    """
        ## A sample hello world route
        This returns Hello world
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return {"message":"Hello World"}


@router.post("/order",status_code=status.HTTP_201_CREATED)
def place_an_order(order:OrderModel,Authorize:AuthJWT=Depends()):
    """
        ## Placing an Order
        This requires the following
        - quantity : integer
        - pizza_size: str
    
    """


    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user=Authorize.get_jwt_subject()

    user=session.query(User).filter(User.username==current_user).first()


    new_order=Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity
    )

    new_order.user=user

    session.add(new_order)

    session.commit()


    response={
        "pizza_size":new_order.pizza_size,
        "quantity":new_order.quantity,
        "id":new_order.id,
        "order_status":new_order.order_status
    }

    return jsonable_encoder(response)



@router.get("/orders")
def list_all_orders(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                  detail="Invalid Token")
    
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username==current_user).first()

    if user.is_staff:
        orders=session.query(Order).all()

        return jsonable_encoder(orders)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                  detail="You are not a superuser")   



@router.get("/orders/{id}")
def get_order_by_id(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                  detail="Invalid Token")

    user=Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        order=session.query(Order).filter(Order.id==id).first()

        return jsonable_encoder(order)  

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                  detail="User not allowed to carry out request")                


@router.get("/user/orders")
def get_user_orders(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                  detail="Invalid Token")

    user=Authorize.get_jwt_subject() 
    current_user=session.query(User).filter(User.username==user).first()

    return jsonable_encoder(current_user.orders)


@router.get('/user/order/{id}/')
async def get_specific_order(id:int,Authorize:AuthJWT=Depends()):
    """
        ## Get a specific order by the currently logged in user
        This returns an order by ID for the currently logged in user
    
    """


    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    subject=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==subject).first()

    orders=current_user.orders

    for o in orders:
        if o.id == id:
            return jsonable_encoder(o)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="No order with such id"
    )


@router.put("/order/update/{id}/")
def update_order(id:int,order:OrderModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                 detail="Invalid Token") 

    order_to_update=session.query(Order).filter(Order.id==id).first()

    order_to_update.quantity=order.quantity
    order_to_update.pizza_size=order.pizza_size

    session.commit()

    response={
                "id":order_to_update.id,
                "quantity":order_to_update.quantity,
                "pizza_size":order_to_update.pizza_size,
                "order_status":order_to_update.order_status,
            }


    return jsonable_encoder(order_to_update)


@router.patch("/order/update/{id}")
def update_order_status(id:int,order:OrderStatusModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                 detail="Invalid Token")

    username=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==username).first()

    if current_user.is_staff:
        order_to_update=session.query(Order).filter(Order.id==id).first()

        order_to_update.order_status=order.order_status 

        session.commit()

        return jsonable_encoder(order_to_update)


@router.delete("/order/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_an_order(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                 detail="Invalid Token")

    order_to_delete=session.query(Order).filter(Order.id==id).first()

    session.delete(order_to_delete)

    session.commit()    

    return order_to_delete         