import aiohttp, asyncio, json
from qiskit.providers.ibmq.job import IBMQJob

from qiskit_job_manager_client.configure import settings
from qiskit_job_manager_client.job_schema import JobStatus


class JobManagerClient:
    def __init__(self, host_url = None, host_port = None, email = None, password = None) -> None:
        self.host_url = None
        self.host_port = None
        self.email = None
        self.password = None
        self.auth_token = None
        self.auth_header = None

        if host_url:
            self.host_url = host_url
        elif settings.HOST:
            self.host_url = settings.HOST

        if host_port:
            self.host_port = host_port
        elif settings.PORT:
            self.host_port = settings.PORT

        if not self.host_url or not self.host_port:
            raise ValueError("Please specify host url and port!")

        self.host_full_url = self.host_url + ":" + str(self.host_port)
        if email:
            self.email = email
        elif settings.EMAIL:
            self.email = settings.EMAIL

        if password:
            self.password = password
        elif settings.PASSWORD:
            self.password = settings.PASSWORD

        if self.email and self.password:
            self.login(self.email, self.password)

        # for print
        self._json_indent = 4


    def login(self, email, password):
        # get token
        form_data_str = f"username={email}&password={password}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        token = asyncio.run(self._request("post", "/auth/jwt/login", return_json=True, handler=self._empty_handler, data=form_data_str, headers=headers))

        self.auth_token = token
        self.auth_header = {"Authorization": f"{token['token_type']} {token['access_token']}"}

    def _check_login(self):
        if not self.auth_header:
            raise ValueError("Please first login!")

    def _add_auth_to_request_kwargs(self, request_kwargs):
        self._check_login()
        if "headers" in request_kwargs.keys():
            request_kwargs["headers"]["Authorization"] = self.auth_header["Authorization"]
        else:
            request_kwargs["headers"]= self.auth_header
        return request_kwargs

    # def test(self):
    #     asyncio.run(self.test_print_user_info_async())

    # async def test_print_user_info_async(self):
    #     response_json = await self._request("get", "/users/me", return_json=True, headers={"Authorization": f"{self.auth_token['token_type']} {self.auth_token['access_token']}"})
    #     print(json.dumps(response_json, indent = self._json_indent))
    #     return response_json


    async def _handler(self, response):
        print("Connect successfully!\n")
        print("Response:")
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])

        # html = await response.text()
        # print("Body:", html)

    async def _empty_handler(self, response):
        # await response.text()
        pass

    async def _request(self, request, url, return_json = False, handler = None, **request_kwargs):
        if not handler:
            handler = self._handler

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
                    await handler(response)
                    if return_json:
                        response_json = await response.json()
            except Exception as e:
                raise e

        if return_json:
            return response_json
        else:
            return True

    def test_connection(self):
        return asyncio.run(self._request("get", "/"))

    async def _auth_request(self, request, url, return_json = False, special_handler_dict = {}, **request_kwargs):
        # because there are two requests: 1. to get the token; 2. to get the response
        # it is better not to reuse request, because it needs two session
        request_kwargs = self._add_auth_to_request_kwargs(request_kwargs)
        return await self._request(request=request, url=url, return_json=return_json, handler=special_handler_dict, **request_kwargs)


    # ------------------------------ User ---------------------------------

    async def create_user_async(self, email, password, ibm_quantum_token = None):
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


    def create_user(self, email, password, ibm_quantum_token = None):
        asyncio.run(self.create_user_async(email=email, password=password, ibm_quantum_token=ibm_quantum_token))


    async def print_user_info_async(self):
        response_json = await self._auth_request("get", "/users/me", return_json=True)
        print(json.dumps(response_json, indent = self._json_indent))
        return response_json


    def print_user_info(self):
        asyncio.run(self.print_user_info_async())


    async def update_user_info_async(self, password = None, ibm_quantum_token = None):
        data = {}
        if password:
            data["password"] = password
            self.password = password
        if ibm_quantum_token:
            data["ibm_quantum_token"] = ibm_quantum_token
        return await self._auth_request("patch", "/users/me", json=data)
    

    def update_user_info(self, password = None, ibm_quantum_token = None):
        asyncio.run(self.update_user_info_async(password=password, ibm_quantum_token=ibm_quantum_token))

    # async def user_delete(self):
    #     user_id = (await (await self._auth_request("get", "/users/me", special_handler_dict={200: self.non_handler})).json())["id"]
    #     return await self._auth_request("delete", "/users/me/", params=user_id)

    # ---------------------------------------------------------------------



    # --------------------------------- Job -------------------------------

    async def print_all_job_info_async(self):
        response_json = await self._auth_request("get", "/job/", return_json=True)
        print(json.dumps(response_json["data"][0], indent = self._json_indent))
        return response_json
    

    def print_all_job_info(self):
        asyncio.run(self.print_all_job_info_async())
    

    async def print_job_info_async(self, job_id):
        self._check_login()

        job_id_list = self._parse_job_list(job_id)
        job_info_list = []
        async with aiohttp.ClientSession(base_url=self.host_full_url) as session:
            # get job information
            is_success = True
            for job_id in job_id_list:
                try:
                    async with session.get("/job/ibm_job_id/id", params={"ibm_job_id": job_id}, headers=self.auth_header) as response:
                        if response.status != 200:
                            is_success = False
                        else:
                            response_json = await response.json()
                            job_info = response_json["data"][0]
                            del job_info["id"]
                            del job_info["owner_id"]
                            job_info_list.append(job_info)
                except Exception as exception:
                    raise exception
        
        job_info = json.dumps(job_info_list, indent = self._json_indent)
        if is_success:
            print(job_info)
        else:
            print("Errors in printing jobs!")
        
        return job_info
    

    def print_job_info(self, job_id):
        asyncio.run(self.print_job_info_async(job_id=job_id))
    

    async def update_job_info_async(self, job_info):
        self._check_login()

        job_info_list = self._parse_job_list(job_info)
        async with aiohttp.ClientSession(base_url=self.host_full_url) as session:
            # update jobs
            is_success = True
            for job_info in job_info_list:
                try:
                    async with session.put("/job/ibm_job_id/id", params={"ibm_job_id": job_info["job_id"]}, json=job_info, headers=self.auth_header) as response:
                        if response.status != 200:
                            is_success = False
                except Exception as exception:
                    raise exception
            
        if is_success:
            print("Successfully update all jobs!")
        else:
            print("Errors in updating jobs!")
        
        return is_success
    

    def update_job_info(self, job_info):
        asyncio.run(self.update_job_info_async(job_info=job_info))
    

    async def delete_job_async(self, job_id):
        self._check_login()
        
        job_id_list = self._parse_job_list(job_id)

        async with aiohttp.ClientSession(base_url=self.host_full_url) as session:
            # delete jobs
            is_success = True
            for job_id in job_id_list:
                try:
                    async with session.delete("/job/ibm_job_id/id", params={"ibm_job_id": job_id}, headers=self.auth_header) as response:
                        if response.status != 200:
                            is_success = False
                except Exception as exception:
                    raise exception
            
        if is_success:
            print("Successfully delete all jobs!")
        else:
            print("Errors in deleting jobs!")
        
        return is_success


    def delete_job(self, job_id):
        asyncio.run(self.delete_job_async(job_id=job_id))


    async def delete_all_job_async(self):
        self._check_login()

        async with aiohttp.ClientSession(base_url=self.host_full_url) as session:
            # get all job ids
            try:
                async with session.get("/job/", headers=self.auth_header) as response:
                    response_json = (await response.json())["data"][0]
            except Exception as exception:
                raise exception

            # delete jobs
            is_success = True
            for job_info in response_json:
                try:
                    async with session.delete("/job/ibm_job_id/id", params={"ibm_job_id": job_info["job_id"]}, headers=self.auth_header) as response:
                        if response.status != 200:
                            is_success = False
                except Exception as exception:
                    raise exception
        
        if is_success:
            print("Successfully delete all jobs!")
        else:
            print("Errors in deleting jobs!")
        
        return is_success


    def delete_all_job(self):
        asyncio.run(self.delete_all_job_async())

    async def register_job_async(self, job, notify_status = None):
        import copy
        job_list = copy.deepcopy(job)
        while not isinstance(job_list, IBMQJob):
            job_list = job_list[0]
        backend_name = job_list.backend().name()
        credentials = job_list.backend().provider().credentials
        provider = [
            credentials.hub,
            credentials.group,
            credentials.project
        ]

        async with aiohttp.ClientSession(base_url=self.host_full_url) as session:
            # register jobs
            is_success = True
            for job_info in self._parse_job_register_info(job, notify_status):
                job_data = {
                    "job_id": job_info[0],
                    "backend_name": backend_name,
                    "provider": provider,
                    "notify_status": job_info[1],
                    "creation_date": job_info[2]
                }

                try:
                    async with session.post("/job/", json=job_data, headers=self.auth_header) as response:
                        if response.status != 200:
                            is_success = False
                except Exception as exception:
                    raise exception
        
        if is_success:
            print("Successfully register all jobs!")
        else:
            print("Errors in register jobs!")
    

    def register_job(self, job, notify_status = None):
        asyncio.run(self.register_job_async(job=job, notify_status=notify_status))

    
    def _parse_job_register_info(self, job, notify_status = None):
        job_info = []

        if isinstance(job, list):
            if notify_status:
                for j, j_s in zip(job, notify_status):
                    job_info += self._parse_job_register_info(j, j_s)
            else:
                for j in job:
                    job_info += self._parse_job_register_info(j, None)
                
        elif isinstance(job, IBMQJob):
            if isinstance(notify_status, str):
                job_info = [[job.job_id(), [notify_status], str(job.creation_date())]]
            elif isinstance(notify_status, list):
                for status in notify_status:
                    if status not in JobStatus:
                        raise ValueError("Status wrong!")
                job_info = [[job.job_id(), notify_status, str(job.creation_date())]]
            elif not notify_status:
                job_info = [[job.job_id(), ["DONE"], str(job.creation_date())]]
            else:
                raise ValueError("Wrong input format!")

        return job_info
    

    def _parse_job_list(self, job_list):
        parsed_job_list = []

        if isinstance(job_list, list):
            for j in job_list:
                parsed_job_list += self._parse_job_list(j)
                
        elif isinstance(job_list, (str, dict)):
            parsed_job_list = [job_list]
        else:
            raise ValueError("Wrong input format!")

        return parsed_job_list
    

    async def register_start_and_done_async(self, job, notify_status = None):
        import copy
        job_list = copy.deepcopy(job)
        while not isinstance(job_list, IBMQJob):
            job_list = job_list[0]
        job_first = job_list

        job_list = copy.deepcopy(job)
        while not isinstance(job_list, IBMQJob):
            job_list = job_list[0]
        job_last = job_list

        backend_name = job_first.backend().name()
        credentials = job_first.backend().provider().credentials
        provider = [
            credentials.hub,
            credentials.group,
            credentials.project
        ]

        if not notify_status:
            notify_status = [["RUNNING"], ["DONE"]]

        async with aiohttp.ClientSession(base_url=self.host_full_url) as session:
            # register jobs
            is_success = True
            for i, job_i in enumerate([job_first, job_last]):
                job_data = {
                    "job_id": job_i.job_id(),
                    "backend_name": backend_name,
                    "provider": provider,
                    "notify_status": notify_status[i],
                    "creation_date": str(job_i.creation_date())
                }

                try:
                    async with session.post("/job/", json=job_data, headers=self.auth_header) as response:
                        if response.status != 200:
                            is_success = False
                except Exception as exception:
                    raise exception
        
        if is_success:
            print("Successfully register all jobs!")
        else:
            print("Errors in register jobs!")
    

    def register_start_and_done(self, job, notify_status = None):
        asyncio.run(self.register_start_and_done_async(job=job, notify_status=notify_status))

    # ---------------------------------------------------------------------


if __name__ == "__main__":
    pass
    # 1. initiate client
    # client = JobManagerClient()
    # client = JobManagerClient(host_url = None, host_port = None, email = None, password = None)
    # client.login(email = "", password = "")

    # 2. user related:
    # client.create_user(email="", password="", ibm_quantum_token="")
    # client.print_user_info()
    # client.update_user_info(password="", ibm_quantum_token="")

    # 3. job related:
    #   (1) add jobs:
    # job_id = [""]
    # job_id = ["", ""]
    # job_id = [["", ""], [""]]

    # from qcutils.credential import load_provider
    # provider = load_provider()
    # backend = provider.get_backend("ibm_lagos")
    # job = [backend.retrieve_job(id) for id in job_id[0]]
    # job += [backend.retrieve_job(job_id[1][0])]

    # client.register_job(job)
    # client.register_start_and_done(job)

    #   (2) job information
    # client.print_all_job_info()
    #  Similar to register job, the job_id can be a list
    # client.print_job_info(job_id)

    #   (3) update job information
    # client.update_job_info({
    #     "job_id": "",
    #     "notify_status": [
    #         "DONE", "CANCELED"
    #     ],
    # })

    #   (4) delete jobs
    # client.delete_job(job_id)
    # client.delete_all_job()

    # The input is a list of IBMQJob objects (the list can be rugged and multi-dimentional)
