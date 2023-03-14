from .db import job_collection
from bson.objectid import ObjectId



def job_helper(job):
    return {
        "id": str(job["_id"]),
        "job_id": job["job_id"],
        "provider": job["provider"],
        "backend_name": job["backend_name"],
        "notify_status": job["notify_status"],
        "creation_date": job["creation_date"],
        "onwer_id": job["onwer_id"]
    }


# Add a new job into to the database
async def add_job(job_data: dict) -> dict:
    job = await job_collection.insert_one(job_data)
    new_job = await job_collection.find_one({"_id": job.inserted_id})
    return job_helper(new_job)


# Retrieve a job with a matching ID
async def retrieve_job(id: str) -> dict:
    job = await job_collection.find_one({"_id": ObjectId(id)})
    if job:
        return job_helper(job)


# Update a job with a matching ID
async def update_job(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    job = await job_collection.find_one({"_id": ObjectId(id)})
    if job:
        updated_job = await job_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_job:
            return True
        return False


# Delete a job from the database
async def delete_job(id: str):
    job = await job_collection.find_one({"_id": ObjectId(id)})
    if job:
        await job_collection.delete_one({"_id": ObjectId(id)})
        return True


# Retrieve all jobs present in the database
async def retrieve_jobs():
    jobs = []
    async for job in job_collection.find():
        jobs.append(job_helper(job))
    return jobs
