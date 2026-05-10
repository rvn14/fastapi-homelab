from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.item import Item
from app.repositories import item_repository
from app.schemas.item import ItemCreate, ItemUpdate


def create_item(db: Session, item_data: ItemCreate) -> Item:
    return item_repository.create_item(db, item_data)


def get_items(db: Session, skip: int = 0, limit: int = 100) -> list[Item]:
    return item_repository.get_items(db, skip, limit)


def get_item(db: Session, item_id: int) -> Item:
    item = item_repository.get_item_by_id(db, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    return item


def update_item(db: Session, item_id: int, item_data: ItemUpdate) -> Item:
    item = get_item(db, item_id)
    return item_repository.update_item(db, item, item_data)


def delete_item(db: Session, item_id: int) -> dict[str, str]:
    item = get_item(db, item_id)
    item_repository.delete_item(db, item)

    return {
        "message": "Item deleted successfully",
    }