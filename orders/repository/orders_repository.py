import uuid

from sqlalchemy.orm import Session

from orders.repository.models import OrderItemModel, OrderModel
from orders.service.orders_service import Order


class OrdersRepository:
    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def add(self, items: list) -> Order:
        record = OrderModel(items=[OrderItemModel(**item) for item in items])
        self.session.add(record)
        return Order(**record.dict(), order_=record)

    def _get(self, id_: uuid.uuid4, **filters) -> OrderModel | None:
        return (
            self.session.query(OrderModel)
            .filter(OrderModel.id == str(id_))
            .filter_by(**filters)
            .first()
        )

    def get(self, id_: uuid.uuid4) -> Order | None:
        order = self._get(id_)
        if order is not None:
            return Order(**order.dict())

    def list(self, limit: int | None = None, **filters) -> list[Order]:
        query = self.session.query(OrderModel)

        if "cancelled" in filters:
            cancelled = filters.pop("cancelled", None)
            if cancelled:
                query = query.filter(OrderModel.status == "cancelled")
            else:
                query = query.filter(OrderModel.status != "cancelled")

        records = query.filter_by(**filters).limit(limit).all()
        return [Order(**record.dict()) for record in records]

    def updated(self, id_: uuid.uuid4, **payload) -> Order:
        record = self._get(id_)

        if "items" in payload:
            for item in record.items:
                self.session.delete(item)
            record.items = [OrderItemModel(**item) for item in payload.pop("items")]

        for key, value in payload.items():
            setattr(record, key, value)

        return Order(**record.dict())

    def delete(self, id_: uuid.uuid4) -> None:
        self.session.delete(self._get(id_))
