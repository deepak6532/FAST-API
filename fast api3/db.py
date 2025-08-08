from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.usermodel import User



MONGO_URI = "mongodb://localhost:27017"  

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["FastApiAuth"]  
    await init_beanie(database=db, document_models=[User])

    

    