from fastapi import FastAPI,HTTPException

from contextlib import asynccontextmanager

from pydantic import BaseModel, EmailStr

import bcrypt

from db import init_db
from models.usermodel import User

import jwt

import random


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)





@app.get("/")
def checking():
    return {"message": "Hello, Good morning..."}


class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    # otp:str
    
    

def generate_otp(length):
    otp = ""
    length = 4

    for _ in range(length):
        random_digit = random.randint(0, 9)
        otp += str(random_digit)    
    return otp



    
@app.post("/signup")
async def signup_user(user: UserSignup):
    
    
    alreadyUser = await User.find_one({"email":user.email})
    if alreadyUser:
        return {"message":"User already exists!"}
    
    
    # otp = generate_otp(4)
    # print("Otp:",otp)
    
    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    # Create a Beanie User document
    user_obj = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        # otp=otp
    )

    await user_obj.insert()
    return {"message": "User signed up successfully",'user':user_obj}



# Login user 

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class loginInfo(BaseModel):
    email:str
    password:str
    
def create_token(email:str):
    payload = {
        "user":email,
        "exp":ACCESS_TOKEN_EXPIRE_MINUTES
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


    
@app.post("/login")
async def login(login_data:loginInfo):
    
    already_user = await User.find_one({"email":login_data.email})
    
    if not already_user:
        raise HTTPException(status_code=404,detail="user not found")
    
    checkPassword = bcrypt.checkpw(login_data.password.encode(), already_user.password.encode())
    
    if not checkPassword:
        raise HTTPException(status_code=404,detail="Incoreect password ")
    
    token = create_token(login_data.email)
    
    return {"message":"login successfull ",
            "token":token
            }