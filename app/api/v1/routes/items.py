from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.services import item_service


router = APIRouter(
    prefix="/items",
    tags=["Items"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/",
    response_model=ItemRead,
    status_code=status.HTTP_201_CREATED,
)
def create_item(
    item_data: ItemCreate,
    db: DatabaseSession,
) -> ItemRead:
    return item_service.create_item(db, item_data)


@router.get(
    "/",
    response_model=list[ItemRead],
)
def get_items(
    db: DatabaseSession,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
) -> list[ItemRead]:
    return item_service.get_items(db, skip, limit)


@router.get(
    "/{item_id}",
    response_model=ItemRead,
)
def get_item(
    item_id: int,
    db: DatabaseSession,
) -> ItemRead:
    return item_service.get_item(db, item_id)


@router.put(
    "/{item_id}",
    response_model=ItemRead,
)
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    db: DatabaseSession,
) -> ItemRead:
    return item_service.update_item(db, item_id, item_data)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_200_OK,
)
def delete_item(
    item_id: int,
    db: DatabaseSession,
) -> dict[str, str]:
    return item_service.delete_item(db, item_id)