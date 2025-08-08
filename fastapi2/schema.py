from pydantic import BaseModel


# class UserBase(BaseModel):
#     name:str
#     email:str
    

# class UserCreate(UserBase):
#     # id:int
#     password:str
    
    


class ProductCreate(BaseModel):
    name:str
    title:str
    category:str
    price:int