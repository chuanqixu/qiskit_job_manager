from bson.objectid import ObjectId
from backend.schemas.user import User
from backend.database.db import job_collection


def job_helper(job):
    return {
        "id": str(job["_id"]),
        "job_id": job["job_id"],
        "provider": job["provider"],
        "backend_name": job["backend_name"],
        "notify_status": job["notify_status"],
        "creation_date": job["creation_date"],
        "owner_id": job["owner_id"]
    }


# Add a new job into to the database
async def add_job(job_data: dict, user: User) -> dict:
    job_data["owner_id"] = str(user.id)
    job = await job_collection.insert_one(job_data)
    new_job = await job_collection.find_one({"_id": job.inserted_id})
    return job_helper(new_job)


# Retrieve a job with a matching ID
async def retrieve_job(id: str, user: User) -> dict:
    if user.is_superuser:
        job = await job_collection.find_one({"_id": ObjectId(id)})
    else:
        job = await job_collection.find_one({"_id": ObjectId(id), "owner_id": str(user.id)})
    if job:
        return job_helper(job)


# Update a job with a matching ID
async def update_job(id: str, data: dict, user: User):
    # Return false if an empty request body is sent.
    if "owner_id" in data.keys():
        return False
    if len(data) < 1:
        return False
    if user.is_superuser:
        job = await job_collection.find_one({"_id": ObjectId(id)})
    else:
        job = await job_collection.find_one({"_id": ObjectId(id), "owner_id": str(user.id)})
    if job:
        updated_job = await job_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_job:
            return True
        return False


# Delete a job from the database
async def delete_job(id: str, user: User):
    if user.is_superuser:
        job = await job_collection.find_one({"_id": ObjectId(id)})
    else:
        job = await job_collection.find_one({"_id": ObjectId(id), "owner_id": str(user.id)})
    if job:
        await job_collection.delete_one({"_id": ObjectId(id)})
        return True


# Retrieve all jobs present in the database
async def retrieve_jobs(user: User):
    jobs = []
    if user.is_superuser:
        async for job in job_collection.find():
            jobs.append(job_helper(job))
    else:
        async for job in job_collection.find({"owner_id": str(user.id)}):
            jobs.append(job_helper(job))
    return jobs

# Update a job with a matching ID
async def update_job_super(id: str, data: dict):
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
async def delete_job_super(id: str):
    job = await job_collection.find_one({"_id": ObjectId(id)})
    if job:
        await job_collection.delete_one({"_id": ObjectId(id)})
        return True
