from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum



class JobStatus(Enum):
    """Class for job status enumerated type."""

    INITIALIZING = "INITIALIZING"
    QUEUED = "QUEUED"
    VALIDATING = "VALIDATING"
    RUNNING = "RUNNING"
    CANCELLED = "CANCELLED"
    DONE = "DONE"
    ERROR = "ERROR"



JOB_FINAL_STATES = (JobStatus.DONE.value, JobStatus.CANCELLED.value, JobStatus.ERROR.value)



class JobSchema(BaseModel):
    job_id: str = Field(min_length=20, max_length=24, default="000000000000000000000000")
    provider: list[str] = Field(min_items=3, max_items=3, default=["hub", "group", "project"])
    backend_name: str = Field(default="ibm_lagos")
    notify_status: list[JobStatus] = Field(default=[JobStatus.DONE])
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
