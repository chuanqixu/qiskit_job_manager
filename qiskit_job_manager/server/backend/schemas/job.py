from typing import Optional
from pydantic import BaseModel, Field



class JobSchema(BaseModel):
    job_id: str = Field(...)
    provider: list[str] = Field(...)
    backend_name: str = Field(...)
    notify_status: list[str] = Field(...)
    creation_date: Optional[str]



class JobRead(BaseModel):
    job_id: Optional[str]
    provider: Optional[list[str]]
    backend_name: Optional[str]
    notify_status: Optional[list[str]]
    creation_date: Optional[str]
    onwer_id: Optional[str]



class JobUpdate(BaseModel):
    job_id: Optional[str]
    provider: Optional[list[str]]
    backend_name: Optional[str]
    notify_status: Optional[list[str]]
    creation_date: Optional[str]



