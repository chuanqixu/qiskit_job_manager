from typing import Optional
from pydantic import BaseModel, EmailStr, Field



class UserSchema(BaseModel):
    email: EmailStr = Field(...)
    is_active: Optional[bool] = True
    is_superuser: bool = False
    ibm_quantum_api: Optional[str] = Field(...)



class UpdateUserModel(BaseModel):
    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    ibm_quantum_api: Optional[str]
