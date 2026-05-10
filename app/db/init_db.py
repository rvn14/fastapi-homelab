from app.db.base import Base
from app.db.session import engine
from app.models.item import Item


def init_db() -> None:
    # Importing the model ensures it is registered before metadata creation.
    _ = Item
    Base.metadata.create_all(bind=engine)
