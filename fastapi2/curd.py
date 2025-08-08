from models.users import User
# from fastapi import HTTPException

from models.product import Product


# create user
async def post_user(user: User):
    new_user = User(**user.model_dump())
    return new_user


# create product

async def create_product(product:Product):
    new_product = Product(**product.model_dump())
    return new_product
