from fastapi import HTTPException
from starlette import status

OrderNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Order not found",
)
