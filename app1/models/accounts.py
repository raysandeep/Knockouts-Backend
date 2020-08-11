  
from pydantic import BaseModel, Field, validator
from datetime import datetime
from uuid import UUID,uuid4
from typing import List,Optional
from db.mongodb import get_nosql_db



class User(BaseModel):
    username : str
    password : str
    salt : str


class UserInDB(User):
    _id : UUID = Field(default_factory=uuid4)
    date_created : datetime= Field(default_factory=datetime.utcnow)

