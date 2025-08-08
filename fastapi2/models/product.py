from beanie import Document
# from pydantic import BaseModel


class Product(Document):
    name:str
    title:str
    category:str
    price:int
    
    
    class Settings:
        name="products"
        