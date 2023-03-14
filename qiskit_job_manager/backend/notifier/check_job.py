import asyncio
from db.db import job_collection
from db.crud_job import job_helper, delete_job, update_job
from db.crud_user import retrieve_user
from qiskit import IBMQ
from configure import settings

from .notifier import Notifier

notifier = Notifier()


async def check_job_status():
    print("Start checking job status...")

    interval = settings.BACKGROUND_INTERVAL

    while True:
        async for job in job_collection.find():
            job_in_db = job_helper(job)
            user = await retrieve_user(job_in_db["onwer_id"])

            provider_info = job_in_db["provider"]
            provider = IBMQ.enable_account(user["ibm_quantum_token"], hub=provider_info[0], group=provider_info[1], project=provider_info[2])
            
            backend = provider.get_backend(job_in_db["backend_name"])
            job = backend.retrieve_job(job_in_db["job_id"])
            job_status = job.status()
            if job_status.name in job_in_db["notify_status"]:
                if job_status.name in ['ERROR', 'CANCELLED', 'DONE']:
                    notifier.send_email(to_addr=user["email"], job_status=job_status.name, job_id=job_in_db["job_id"])
                    await delete_job(job_in_db["id"])
                else:
                    notifier.send_email(to_addr=user["email"], job_status=job_status.name, job_id=job_in_db["job_id"])
                    job_in_db["notify_status"].remove(job_status.name)
                    update_job(job_in_db["id"], job_in_db)

            IBMQ.disable_account()

            await asyncio.sleep(interval)
