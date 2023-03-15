from beanie import PydanticObjectId
from fastapi_users import schemas
from typing import Optional
from fastapi_users.db import BeanieBaseUser



class User(BeanieBaseUser[PydanticObjectId]):
    ibm_quantum_token: Optional[str]

class UserRead(schemas.BaseUser[PydanticObjectId]):
    ibm_quantum_token: Optional[str]


class UserCreate(schemas.BaseUserCreate):
    ibm_quantum_token: Optional[str]


class UserUpdate(schemas.BaseUserUpdate):
    ibm_quantum_token: Optional[str]
