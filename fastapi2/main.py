from fastapi import FastAPI, HTTPException 
from contextlib import asynccontextmanager

from db import init_db

from  models.users  import User

from pydantic import BaseModel
from bson import ObjectId
 
 
from models.product import Product # product model import


app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def checking():
    return {"message": "Hello..."}




@app.post("/createusers")
async def post_user(user: User):

    new_user = User(**user.model_dump())
    await new_user.insert()
    return new_user


@app.get('/getusers')
async def get_userr():
    get_user = await User.find_all().to_list()
    return get_user
    
    



# get one user bases of name
class UserRequest(BaseModel):
    username: str


@app.post("/getoneuser")
async def get_one_user(request: UserRequest):
    print("username:", request.username)
    
    get_one_user = await User.find_one({"username": request.username})
    
    if not get_one_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "Send data success", "data": get_one_user}



    
    
    
@app.put("/updateuser/{id}")
async def update_user(id: str, user_data: User):
    try:
        obj_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    user = await User.find_one(User.id == obj_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_fields = user_data.model_dump()
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No update data provided")

    await user.update({"$set": update_fields})

    updated_user = await User.find_one(User.id == obj_id)
    return {"message": "User updated successfully", "user": updated_user}





# delete api

@app.delete("/deleteuser/{id}")
async def delete_user(id: str):
    try:
        obj_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    user = await User.find_one(User.id == obj_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()

    return {"message": "User deleted successfully"}










# Product api


@app.get("/product")

async def check_product():
    return {"message":"Product model created ..."}



# create product


@app.post("/CreateProduct")
async def create_product(product:Product):
    new_product = Product(**product.model_dump())
    await new_product.insert()
    return new_product


# get product 

@app.get("/getproduct")
async def get_product():
    get_product =  await Product.find().to_list()
    return get_product


# get product by name and  same as category

class product_request(BaseModel):
    name:str
    

@app.post("/getproduct_name")
async def get_product_by_name(product:product_request):
    
        get_product_name = await Product.find({"name":product.name}).to_list()
    
        if not get_product_name:
            raise HTTPException(status_code=404,detail="product not found")

        return {'message':"Success find..","product":get_product_name}
    
    




# update product 

@app.put("/updateProduct/{id}")
async def update_product(id:str,product_data:Product):
    try:
        obj_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=404,detail="invalid id")
    
    product = await Product.find_one(Product.id == obj_id)
    
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")
    
    
    update_data   =  product_data.model_dump()
    
    if not update_data:
        raise HTTPException(status_code=404,detail="update data not provide ")
    
    await product.update({"$set":update_data})
    
    new_data = await Product.find_one(Product.id == obj_id)
    return {"message":"product update successfully ",
            "Updated product":new_data}
    
    