import aiohttp, asyncio
from qiskit.providers.ibmq.job import IBMQJob
from qiskit.providers.backend import BackendV1 as Backend

from qiskit_job_manager_client.configure import settings
from qiskit_job_manager_client.job_schema import JobStatus


class JobManagerClient:
    def __init__(self, host_url = None, host_port = None, email = None, password = None) -> None:
        if host_url or not settings.HOST:
            self.host_url = host_url
        else:
            self.host_url = settings.HOST
        if host_port or not settings.PORT:
            self.host_port = host_port
        else:
            self.host_port = settings.PORT
        self.host_full_url = self.host_url + ":" + str(self.host_port)
        if email or not settings.EMAIL:
            self.email = email
        else:
            self.email = settings.EMAIL
        if password or not settings.PASSWORD:
            self.password = password
        else:
            self.password = settings.PASSWORD

    async def _handler(self, response):
        print("Connect successfully!\n")
        print("Response:")
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])

        html = await response.text()
        print("Body:", html)
    
    async def _non_handler(self, response):
        await response.text()

    async def _request(self, request, url, special_handler_dict = {}, **request_kwargs):
        if not isinstance(special_handler_dict, dict):
            raise ValueError("handle_dict should be a dict object!")
        
        async with aiohttp.ClientSession(base_url=self.host_full_url) as session:
            if request == "get":
                request_func = session.get
            elif request == "post":
                request_func = session.post
            elif request == "put":
                request_func = session.put
            elif request == "delete":
                request_func = session.delete
            elif request == "patch":
                request_func = session.patch
            else:
                raise ValueError("Input request wrong!")
            
            try:
                async with request_func(url, **request_kwargs) as response:
                    if response.status in special_handler_dict.keys():
                        await special_handler_dict[response.status](response)
                    else:
                        await self._handler(response)
            except Exception as e:
                raise e
        
        return response

    async def test_connection(self):
        return await self._request("get", "/")
    
    async def _get_token(self):
        form_data_str = f"username={self.email}&password={self.password}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        token_response = await self._request("post", "/auth/jwt/login", special_handler_dict={200: self._non_handler}, data=form_data_str, headers=headers)
        token = await token_response.json()
        return (token["token_type"], token["access_token"])

    async def _auth_request(self, request, url, special_handler_dict = {}, **request_kwargs):
        token = await self._get_token()
        if "headers" in request_kwargs.keys():
            request_kwargs["headers"]["Authorization"] = f"{token[0]} {token[1]}"
        else:
            request_kwargs["headers"]= {"Authorization": f"{token[0]} {token[1]}"}
        return await self._request(request=request, url=url, special_handler_dict=special_handler_dict, **request_kwargs)



    # ------------------------------ User ---------------------------------

    async def create_user(self, email, password, ibm_quantum_token = None):
        data = {
            "email": email,
            "password": password,
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "ibm_quantum_token": ibm_quantum_token
        }
        self.email = email
        self.password = password
        return await self._request("post", "/auth/register", json = data)

    async def print_user_info(self):
        return await self._auth_request("get", "/users/me")

    async def update_user_info(self, password = None, ibm_quantum_token = None):
        data = {}
        if password:
            data["password"] = password
            self.password = password
        if ibm_quantum_token:
            data["ibm_quantum_token"] = ibm_quantum_token
        return await self._auth_request("patch", "/users/me", json=data)
    
    # async def user_delete(self):
    #     user_id = (await (await self._auth_request("get", "/users/me", special_handler_dict={200: self.non_handler})).json())["id"]
    #     return await self._auth_request("delete", "/users/me/", params=user_id)

    # ---------------------------------------------------------------------



    # --------------------------------- Job -------------------------------

    async def print_all_job_info(self):
        return await self._auth_request("get", "/job/")
    
    async def print_job_info(self, job_id):
        return await self._auth_request("get", "/job/ibm_id", params=job_id)
    
    async def delete_job(self, job_id):
        return await self._auth_request("delete", "/job/ibm_id", params=job_id)
    
    async def _delete_job(self, job_id):
        return await self._auth_request("delete", "/job/", params=job_id)

    async def delete_all_job(self):
        job_list = await self.print_all_job_info()
        for job in job_list():
            await self._delete_job(job["id"])

    async def register_job(self, job, notify_status = None, backend_name = None)
        if not backend_name:
            while not isinstance(job, IBMQJob):
                job = job[0]
            backend_name = job.backend().name()
            credentials = job.backend().provider().credentials
            provider = {
                credentials.hub,
                credentials.group,
                credentials.project
            }

        async with aiohttp.ClientSession(base_url=self.host_full_url) as session:
            
            # get token
            form_data_str = f"username={self.email}&password={self.password}"
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            token_response = await self._request("post", "/auth/jwt/login", special_handler_dict={200: self._non_handler}, data=form_data_str, headers=headers)
            token = await token_response.json()
            headers= {"Authorization": f"{token[0]} {token[1]}"}

            # register jobs
            for job_info in self._parse_job_info(job, notify_status):
                job_data = {
                    "job_id": job_info[0],
                    "backend_name": backend_name,
                    "notify_status": job_info[1],
                    "creation_date": str(job.creation_date())
                }

                try:
                    async with session.post("/job/", json=job_data, headers=headers)
                except Exception as e:
                    raise e
        
        print("Successfully register all jobs!")
    
    def _parse_job_info(self, job, notify_status = None):
        job_info = []

        if isinstance(job, list):
            if not notify_status:
                for j, j_s in zip(job, notify_status):
                    job_info += self._parse_job_info(j, j_s)
            else:
                for j in job:
                    job_info += self._parse_job_info(j, notify_status)
                
        elif isinstance(job, IBMQJob):
            if isinstance(notify_status, str):
                job_info = [job.job_id(), [notify_status]]
            elif isinstance(notify_status, list):
                for status in notify_status:
                    if status not in JobStatus:
                        raise ValueError("Status wrong!")
                job_info = [job.job_id(), notify_status]
            elif not notify_status:
                job_info = [job.job_id(), ["DONE"]]
            else:
                raise ValueError("Wrong input format!")

        return job_info

    # ---------------------------------------------------------------------


if __name__ == "__main__":
    client = JobManagerClient()
    asyncio.run(client.print_all_job_info())


