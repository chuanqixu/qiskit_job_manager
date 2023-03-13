
def check_job_status(interval = None):
    if not interval:
        interval = 2

    while True:
        sending_list = []
        for backend_name, job_info in self.notify_list.items():
            backend = self.ibm_provider.get_backend(backend_name)
            for job_id, status_to_notify in job_info:
                job = backend.retrieve_job(job_id)
                job_status = job.status()
                if job_status.name in status_to_notify:
                    sending_list.append([job_id, job_status.name])
                    if job_status.name in ['ERROR', 'CANCELLED', 'DONE']:
                        self.notify_list[backend_name].remove([job_id, status_to_notify])
                    else:
                        self.notify_list[backend_name].remove(job_status.name)
        
        for sending_info in sending_list:
            self.notifier.send_email(job_status=sending_info[1], job_id=sending_info[0])
        
        await asyncio.sleep(interval)