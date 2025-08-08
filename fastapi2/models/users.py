from beanie import Document
# from pydantic import BaseModel


class User(Document):
    username: str
    email: str
    age: int
    password: str

    class Settings:
        name = "users"