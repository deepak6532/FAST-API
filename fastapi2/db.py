

from pymongo import AsyncMongoClient
from models.users import User
from beanie import init_beanie

from models.product import Product      # import the product model 


DATABASE_URL  = "mongodb://localhost:27017/fastDatabase"

async def init_db():
    client = AsyncMongoClient(DATABASE_URL)
    db = client.get_database('fastDatabase')  # Use the database name you want
    await init_beanie(db, document_models=[User])
    
    await init_beanie(db,document_models=[Product])  #product model