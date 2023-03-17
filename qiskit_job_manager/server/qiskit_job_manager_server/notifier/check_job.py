import asyncio
from bson.objectid import ObjectId

from ..configure import settings
from ..database.db import job_collection, user_collection
from ..database.crud_job import job_helper, delete_job_super, update_job_super
from ..schemas.job import JOB_FINAL_STATES
from .notifier import Notifier

from qiskit import IBMQ
from qiskit.providers.ibmq.api.exceptions import RequestsApiError
from qiskit.providers.ibmq import IBMQProviderError, IBMQBackendApiError
from qiskit.providers import QiskitBackendNotFoundError


notifier = Notifier()


async def check_job_status():
    print("Start checking job status...")

    interval = settings.BACKGROUND_INTERVAL

    while True:
        async for job in job_collection.find():
            job_in_db = job_helper(job)
            user = await user_collection.find_one({"_id": ObjectId(job_in_db["owner_id"])})
            provider_info = job_in_db["provider"]

            try:
                IBMQ.enable_account(user["ibm_quantum_token"])
            except RequestsApiError:
                notifier.send_email(to_addr=user["email"], subject="IBM Quantum Token is not Valid")
                await delete_job_super(job_in_db["id"])
                continue

            try:
                provider = IBMQ.get_provider(hub=provider_info[0], group=provider_info[1], project=provider_info[2])
            except IBMQProviderError:
                notifier.send_email(to_addr=user["email"], subject="Job Provider is not Valid")
                await delete_job_super(job_in_db["id"])
                continue
            
            try:
                backend = provider.get_backend(job_in_db["backend_name"])
            except QiskitBackendNotFoundError:
                notifier.send_email(to_addr=user["email"], subject="Backend is Not Found")
                await delete_job_super(job_in_db["id"])
                continue

            try:
                job = backend.retrieve_job(job_in_db["job_id"])
            except IBMQBackendApiError:
                notifier.send_email(to_addr=user["email"], subject="Job is Not Found")
                await delete_job_super(job_in_db["id"])
                continue

            job_status = job.status()
            if job_status.name in job_in_db["notify_status"]:
                subject = f"IBM Quantum Job Status: {job_status.name} -- Job ID {job_in_db['job_id']}"
                if job_status.name in JOB_FINAL_STATES:
                    notifier.send_email(to_addr=user["email"], subject=subject)
                    await delete_job_super(job_in_db["id"])
                else:
                    notifier.send_email(to_addr=user["email"], subject=subject)
                    job_in_db["notify_status"].remove(job_status.name)
                    await update_job_super(job_in_db["id"], job_in_db)

            IBMQ.disable_account()

            await asyncio.sleep(interval)
