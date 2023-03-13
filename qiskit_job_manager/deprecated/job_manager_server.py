import asyncio, pickle
from .credential import load_provider

from .notifier import Notifier



class JobManagerServer:
    def __init__(self, host_info, ibm_provider = None) -> None:
        self.notify_list = {} # {backend_name: [job_id, [status_to_notify, ]]}
        self.notifier = Notifier()
        self.host_info = host_info
        if not ibm_provider:
            ibm_provider = load_provider()
        self.ibm_provider = ibm_provider

    async def accept(self, reader, writer):
        request = None
        # while request != 'quit':
        request = await reader.read(1024)
        # if not request:
        #     break
        backend_name, job_info = pickle.loads(request)
        if backend_name in self.notify_list.keys():
            self.notify_list[backend_name] += job_info
        else:
            self.notify_list[backend_name] = job_info

        writer.close()
    
    async def check_job(self, interval = None):
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

    async def run(self):
        task_check_job = asyncio.create_task(self.check_job())
        server = await asyncio.start_server(self.accept, self.host_info[0], self.host_info[1])
        async with server:
            await server.serve_forever()
        # task_accept = asyncio.create_task(self.accept())
