from typing import Optional
from pydantic import BaseModel, EmailStr, Field



class JobSchema(BaseModel):
    job_id: str = Field(...)
    provider: list[str] = Field(...)
    backend_name: str = Field(...)
    notify_status: list[str] = Field(...)
    creation_date: Optional[str]
    onwer_id: str = Field(...)



class UpdateJobModel(BaseModel):
    job_id: Optional[str]
    provider: Optional[list[str]]
    backend_name: Optional[str]
    notify_status: Optional[list[str]]
    creation_date: Optional[str]
    onwer_id: Optional[str]
