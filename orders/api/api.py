import datetime
import uuid
from http import HTTPStatus

from starlette import status
from starlette.responses import Response

from orders.api.exceptions import OrderNotFound
from orders.api.schemas import CreateOrderSchema, GetOrderSchema, GetOrdersSchema
from orders.app import app

ORDERS = []


@app.get("/orders", response_model=GetOrdersSchema)
def get_orders():
    return {"orders": ORDERS}


@app.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
)
def create_order(order_details: CreateOrderSchema):
    order = order_details.model_dump()
    order["id"] = uuid.uuid4()
    order["created"] = datetime.datetime.now()
    order["status"] = "created"
    ORDERS.append(order)
    return order


@app.get("/orders/{order_id}", response_model=GetOrderSchema)
def get_order(order_id: uuid.UUID):
    for order in ORDERS:
        if order["id"] == order_id:
            return order
    raise OrderNotFound


@app.put("/orders/{order_id}", response_model=GetOrderSchema)
def update_order(order_id: uuid.UUID, order_details: CreateOrderSchema):
    for order in ORDERS:
        if order["id"] == order_id:
            order.update(order_details.model_dump())
            return order
    raise OrderNotFound


@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: uuid.UUID):
    for index, order in enumerate(ORDERS):
        if order["id"] == order_id:
            ORDERS.pop(index)
            return Response(status_code=HTTPStatus.NO_CONTENT.value)
    raise OrderNotFound


@app.post("/orders/{order_id}/cancel", response_model=GetOrderSchema)
def cancel_order(order_id: uuid.UUID):
    for order in ORDERS:
        if order["id"] == order_id:
            order["status"] = "cancelled"
            return order
    raise OrderNotFound


@app.post("/orders/{order_id}/pay", response_model=GetOrderSchema)
def pay_order(order_id: uuid.UUID):
    for order in ORDERS:
        if order["id"] == order_id:
            order["status"] = "progress"
            return order
    raise OrderNotFound
