from fastapi import FastAPI, Response, HTTPException
from models import Mushroom, Basket, BasketPut
from starlette import status
from db import find
import uvicorn


mushrooms: list[Mushroom] = []
baskets: list[Basket] = []

app = FastAPI()


@app.post("/mushrooms/create", status_code=status.HTTP_201_CREATED)
async def mushroom_create(mushroom: Mushroom) -> Response:
    if not find(mushrooms, mushroom.id):
        mushrooms.append(mushroom)
        return mushroom
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="Mushroom already exists"
    )


@app.put("/mushrooms/update", status_code=status.HTTP_201_CREATED)
async def mushroom_update(mushroom: Mushroom) -> Response:
    if not find(mushrooms, mushroom.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mushroom not found"
        )

    mushrooms.remove(find(mushrooms, mushroom.id))
    mushrooms.append(mushroom)

    for basket in baskets:
        for basket_mushroom in basket.mushrooms:
            if basket_mushroom.id == mushroom.id:
                basket_mushroom.__dict__.update(mushroom.model_dump())

    return mushroom


@app.get("/mushrooms/get/{item_id}")
async def mushroom_get(item_id: int) -> Response:
    result = find(mushrooms, item_id)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/baskets/create", status_code=status.HTTP_201_CREATED)
async def basket_create(basket: Basket) -> Response:
    if not find(baskets, basket.id):
        baskets.append(basket)
        return basket
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="Basket already exists"
    )


@app.post("/baskets/put/", status_code=status.HTTP_201_CREATED)
async def basket_put(basket_put: BasketPut) -> Response:
    basket = find(baskets, basket_put.basket_id)
    mushroom = find(mushrooms, basket_put.mushroom_id)
    if not basket or not mushroom:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bad request. {basket=} {mushroom=}",
        )
    if (sum(m.weight for m in basket.mushrooms) + mushroom.weight) > basket.capacity:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail="Basket overflow"
        )
    basket.mushrooms.append(mushroom)
    return basket


@app.delete("/baskets/delete_mushroom/", status_code=status.HTTP_201_CREATED)
async def basket_delete_mushroom(basket_put: BasketPut) -> Response:
    basket = find(baskets, basket_put.basket_id)
    mushroom = find(mushrooms, basket_put.mushroom_id)
    if not basket or not mushroom:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bad request. {basket=} {mushroom=}",
        )
    basket.mushrooms.remove(mushroom)
    return basket


@app.get("/baskets/get/{basket_id}")
async def basket_get(basket_id: int) -> Response:
    result = find(baskets, basket_id)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Basket not found"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
