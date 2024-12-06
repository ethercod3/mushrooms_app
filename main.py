from fastapi import FastAPI, Response, status
from models import Mushroom, Basket, BasketPut
from db import find
import uvicorn


mushrooms: list[Mushroom] = []
baskets: list[Basket] = []

app = FastAPI()


@app.post("/mushrooms/create")
async def mushroom_create(mushroom: Mushroom, response: Response) -> Response:
    if not find(mushrooms, mushroom.id):
        mushrooms.append(mushroom)
        response.status_code = status.HTTP_201_CREATED
        return mushroom
    else:
        response.status_code = status.HTTP_409_CONFLICT
        return "Mushroom already exists"


@app.put("/mushrooms/update")
async def mushroom_update(mushroom: Mushroom, response: Response) -> Response:
    if not find(mushrooms, mushroom.id):
        response.status_code = status.HTTP_404_NOT_FOUND
        return "Item not found"
    else:
        mushrooms.remove(find(mushrooms, mushroom.id))
        mushrooms.append(mushroom)

        for basket in baskets:
            for basket_mushroom in basket.mushrooms:
                if basket_mushroom.id == mushroom.id:
                    basket_mushroom.__dict__.update(mushroom.model_dump())

        response.status_code = status.HTTP_201_CREATED
        return mushroom


@app.get("/mushrooms/get/{item_id}")
async def mushroom_get(item_id: int, response: Response) -> Response:
    result = find(mushrooms, item_id)
    if result:
        response.status_code = status.HTTP_200_OK
        return result
    else:
        response.status_code = status.HTTP_404_NOT_FOUND


@app.post("/baskets/create")
async def basket_create(basket: Basket, response: Response) -> Response:
    if not find(baskets, basket.id):
        baskets.append(basket)
        response.status_code = status.HTTP_200_OK
        return basket
    else:
        response.status_code = status.HTTP_409_CONFLICT
        return "Basket already exists"


@app.post("/baskets/put/")
async def basket_put(basket_put: BasketPut, response: Response) -> Response:
    basket = find(baskets, basket_put.basket_id)
    mushroom = find(mushrooms, basket_put.mushroom_id)
    if not basket or not mushroom:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Bad request. {basket=} {mushroom=}"
    if (sum(m.weight for m in basket.mushrooms) + mushroom.weight) > basket.capacity:
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return "Basket overflow"
    basket.mushrooms.append(mushroom)
    return basket


@app.delete("/baskets/delete_mushroom/")
async def basket_delete_mushroom(basket_put: BasketPut, response: Response) -> Response:
    basket = find(baskets, basket_put.basket_id)
    mushroom = find(mushrooms, basket_put.mushroom_id)
    if not basket or not mushroom:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Bad request. {basket=} {mushroom=}"
    basket.mushrooms.remove(mushroom)
    return basket


@app.get("/baskets/get/{basket_id}")
async def basket_get(basket_id: int, response: Response) -> Response:
    result = find(baskets, basket_id)
    if result:
        response.status_code = status.HTTP_200_OK
        return result
    else:
        response.status_code = status.HTTP_404_NOT_FOUND


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
