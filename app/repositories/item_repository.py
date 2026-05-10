from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


def create_item(db: Session, item_data: ItemCreate) -> Item:
    item = Item(**item_data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_items(db: Session, skip: int = 0, limit: int = 100) -> list[Item]:
    statement = select(Item).offset(skip).limit(limit)
    return list(db.scalars(statement))


def get_item_by_id(db: Session, item_id: int) -> Item | None:
    return db.get(Item, item_id)


def update_item(db: Session, item: Item, item_data: ItemUpdate) -> Item:
    updates = item_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(item, field, value)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item: Item) -> None:
    db.delete(item)
    db.commit()
