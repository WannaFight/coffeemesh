import datetime
import uuid


class OrdersService:
    def __init__(self, orders_repository) -> None:
        self.orders_repository = orders_repository

    def place_order(self, items):
        pass

    def get_order(self, order_id):
        pass

    def updated_order(self, order_id):
        pass

    def list_orders(self, **filters):
        pass

    def pay_order(self, order_id):
        pass

    def cancel_order(self, order_id):
        pass


class OrderItem:
    def __init__(self, id: uuid.uuid4, product: str, quantity: int, size: str):
        self.id = id
        self.product = product
        self.quantity = quantity


class Order:
    def __init__(
        self,
        id: uuid.uuid4,
        created: datetime.datetime,
        items: list,
        status: str,
        schedule_id: uuid.uuid4 | None = None,
        delivery_id: uuid.uuid4 | None = None,
        order_=None,
    ):
        self._id = id
        self._created = created
        self.items = [OrderItem(**item) for item in items]
        self._status = status
        self.schedule_id = schedule_id
        self.delivery_id = delivery_id
        self._order = order_

    @property
    def id(self) -> uuid.uuid4:
        return self._id or self._order.id

    @property
    def created(self) -> datetime.datetime:
        return self._created or self._order.created

    @property
    def status(self) -> str:
        return self._status or self._order.status
