from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from ..database.crud_job import (
    add_job,
    delete_job,
    retrieve_job,
    retrieve_jobs,
    update_job,
)
from ..schemas.job import (
    JobSchema,
    JobRead,
    JobUpdate,
)

from ..schemas.response import (
    ErrorResponseModel,
    ResponseModel,
)

from fastapi_users.db import BeanieUserDatabase
from ..routers.user_manager import current_active_user


job_router = APIRouter()


@job_router.post("/", response_description="Job data added into the database")
async def add_job_data(job: JobSchema = Body(...), user: BeanieUserDatabase = Depends(current_active_user)):
    job = jsonable_encoder(job)
    new_job = await add_job(job, user)
    return ResponseModel(new_job, "Job added successfully.")


@job_router.get("/", response_description="Jobs retrieved")
async def get_jobs(user: BeanieUserDatabase = Depends(current_active_user)):
    jobs = await retrieve_jobs(user)
    if jobs:
        return ResponseModel(jobs, "Jobs data retrieved successfully")
    return ResponseModel(jobs, "Empty list returned")


@job_router.get("/{id}", response_description="Job data retrieved")
async def get_job_data(id, user: BeanieUserDatabase = Depends(current_active_user)):
    job = await retrieve_job(id, user)
    if job:
        return ResponseModel(job, "job data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Job doesn't exist.")


@job_router.put("/{id}")
async def update_job_data(id: str, req: JobUpdate = Body(...), user: BeanieUserDatabase = Depends(current_active_user)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_job = await update_job(id, req, user)
    if updated_job:
        return ResponseModel(
            "Job with ID: {} name update is successful".format(id),
            "Job name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the job data.",
    )


@job_router.delete("/{id}", response_description="Job data deleted from the database")
async def delete_job_data(id: str, user: BeanieUserDatabase = Depends(current_active_user)):
    deleted_job = await delete_job(id, user)
    if deleted_job:
        return ResponseModel(
            "Job with ID: {} removed".format(id), "Job deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Job with id {0} doesn't exist".format(id)
    )
