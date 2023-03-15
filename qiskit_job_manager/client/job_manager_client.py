import socket, pickle
from qiskit.providers.ibmq.job import IBMQJob
from qiskit.providers.backend import BackendV1 as Backend

import aiohttp, asyncio

class JobManagerClient:
    def __init__(self, host_url, host_port) -> None:
        self.host_url = host_url
        self.host_port = host_port
        self.host_full_url = host_url + ":" + str(host_port)
        # self.host_info = host_info
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.connect(self.host_info)
    
    async def test_log(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.host_full_url) as response:
                if response.status == 200:
                    print("Connect successfully!\n")
                    print("Status:", response.status)
                    print("Content-type:", response.headers['content-type'])

                    html = await response.text()
                    print("Body:", html)
                    return True
                else:
                    raise ConnectionError(f"Connect failed! Status: {response.status}")
    
    async def create_user(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.host_full_url) as response:
                if response.status == 200:
                    print("Connect successfully!\n")
                    print("Status:", response.status)
                    print("Content-type:", response.headers['content-type'])

                    html = await response.text()
                    print("Body:", html)
                    return True
                else:
                    raise ConnectionError(f"Connect failed! Status: {response.status}")

    # def register_job(self, backend_name, job, job_status = None):
    #     data = self._parse_job_info(backend_name, job, job_status)
    #     self.sock.send(pickle.dumps(data))
    #     import time
    #     time.sleep(0.5)

    # def send(self, msg):
    #     self.sock.send(pickle.dumps(msg))
    
    def _parse_job_info(self, backend_name, job, job_status = None):
        job_info = []

        # if isinstance(job, list) and isinstance(job_status, list) and len(job) == len(job_status):
        #     pass
        # elif isinstance(job, str) or isinstance(job, IBMJob):
        #     pass
        # else:
        #     raise Exception("Input wrong!")
        
        if isinstance(backend_name, Backend):
            backend_name = backend_name.configuration().backend_name

        if isinstance(job, list):
            if not job_status:
                for j in job:
                    job_info += self._parse_job_info(backend_name, j, job_status)[1]
            else:
                for j, j_s in zip(job, job_status):
                    job_info += self._parse_job_info(backend_name, j, j_s)[1]
        elif isinstance(job, str):
            if isinstance(job_status, str):
                job_info = [job, [job_status]]
            elif isinstance(job_status, list) and isinstance(job_status[0], str):
                job_info = [job, job_status]
            elif not job_status:
                job_info = [job, ["DONE"]]
            else:
                raise Exception("Wrong input format!")
        elif isinstance(job, IBMQJob):
            if isinstance(job_status, str):
                job_info = [job.job_id(), [job_status]]
            elif isinstance(job_status, list) and isinstance(job_status[0], str):
                job_info = [job.job_id(), job_status]
            elif not job_status:
                job_info = [job.job_id(), ["DONE"]]
            else:
                raise Exception("Wrong input format!")

        if not isinstance(job_info[0], list):
            job_info = [job_info]
        return [backend_name, job_info]

if __name__ == "__main__":
    client = JobManagerClient("http://127.0.0.1", 80)
    asyncio.run(client.test_log())
