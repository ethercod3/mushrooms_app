from models import Basket, Mushroom


def find(items: list[Basket | Mushroom], id: int):
    for item in items:
        if item.id == id:
            return item
    return
