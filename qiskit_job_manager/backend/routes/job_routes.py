from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from db.crud_job import (
    add_job,
    delete_job,
    retrieve_job,
    retrieve_jobs,
    update_job,
)
from schemas.job import (
    JobSchema,
    UpdateJobModel,
)

from schemas.response import (
    ErrorResponseModel,
    ResponseModel,
)

job_router = APIRouter()


@job_router.post("/", response_description="Job data added into the database")
async def add_job_data(job: JobSchema = Body(...)):
    job = jsonable_encoder(job)
    new_job = await add_job(job)
    return ResponseModel(new_job, "Job added successfully.")


@job_router.get("/", response_description="Jobs retrieved")
async def get_jobs():
    jobs = await retrieve_jobs()
    if jobs:
        return ResponseModel(jobs, "Jobs data retrieved successfully")
    return ResponseModel(jobs, "Empty list returned")


@job_router.get("/{id}", response_description="Job data retrieved")
async def get_job_data(id):
    job = await retrieve_job(id)
    if job:
        return ResponseModel(job, "job data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Job doesn't exist.")


@job_router.put("/{id}")
async def update_job_data(id: str, req: UpdateJobModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_job = await update_job(id, req)
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
async def delete_job_data(id: str):
    deleted_job = await delete_job(id)
    if deleted_job:
        return ResponseModel(
            "Job with ID: {} removed".format(id), "Job deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Job with id {0} doesn't exist".format(id)
    )
