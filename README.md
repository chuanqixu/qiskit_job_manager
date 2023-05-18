# qiskit_job_manager

A package for setting up a **server** for the email notification service, and the **client** for interacting with the server.

**Note: While users' passwords are stored only with their hash values, IBM Quantum Token is stored with the original values because the server needs to log in to the account to retrieve the job status!**

# Server

## Feature

- [x] Basic APIs for IBM Quantum job management based on [FastAPI](https://github.com/tiangolo/fastapi), including sending emails when job status meets the requirements.
- [x] Ready-to-use register, login, reset passwords, and authentication based on [FastAPI Users](https://github.com/fastapi-users/fastapi-users#readme).
- [x] Based on [MongoDB](https://www.mongodb.com/) for data storage.

## Set up

1. Install qiskit_job_manager_server package:
   1. Change to the path `qiskit_job_manager/server`:
      ```bash
      cd qiskit_job_manager/server
      ```
   2. Install the package by entering the command:
      ```bash
      pip install .
      ```
2. Configure the environment variables:
   1. Change to the path `qiskit_job_manager/server/qiskit_job_manager_server/configure`:
      ```bash
      cd qiskit_job_manager/server/qiskit_job_manager_server/configure
      ```
   2. Under the path, copy `.env_example` to `.env` by entering the command:
      ```bash
      cp .env_example .env
      ```
   3. Edit `.env` to change the environment variables.

## Usage

Start the server by choosing one of the ways:
1. Directly run the main file by entering the command:
     ```bash
     python qiskit_job_manager/server/qiskit_job_manager_server/main.py
     ```
2.  Run the code with the main function:
    ```python
     from qiskit_job_manager_server import run_server

     run_server()
    ```

## Running with Docker

Example configuration files: [dockerfile for application](qiskit_job_manager/server/dockerfile), [dockerfile for Nginx](qiskit_job_manager/server/nginx/dockerfile_nginx_example), [docker-compose.yaml](qiskit_job_manager/server/docker-compose.yaml), and [Nginx Configureation](qiskit_job_manager/server/nginx/nginx.conf) are in [qiskit_job_manager/server](qiskit_job_manager/server). This example hosts the server with [Nginx](https://www.nginx.com/). You can specify your own stacks for hosting by changing [docker-compose.yaml](qiskit_job_manager/server/docker-compose.yaml).

### Steps for the example hosting:

1. Change directory to `qiskit_job_manager/server/`:
   ```bash
   cd qiskit_job_manager/server
   ```
2. Create your dockerfile for nginx or copy the example:
   ```bash
   cp nginx/dockerfile_nginx_example nginx/dockerfile
   ```
3. If you want to support HTTPS, comment out the `COPY` commands for the SSL certificate in `nginx/dockerfile`, and provide your SSL certificate. Comment out and change SSL-related attributes in [Nginx Configureation](qiskit_job_manager/server/nginx/nginx.conf). If you would like different names for the certificate in Docker container, remember to change related attributes in [Nginx Configureation](qiskit_job_manager/server/nginx/nginx.conf).
4. Review [dockerfile for application](qiskit_job_manager/server/dockerfile), [dockerfile for Nginx](qiskit_job_manager/server/nginx/dockerfile_nginx_example), [docker-compose.yaml](qiskit_job_manager/server/docker-compose.yaml), and [Nginx Configureation](qiskit_job_manager/server/nginx/nginx.conf) and customize the files. If you do not change the IP address mapping, your application IP address to be viewed by the external should be `0.0.0.0`. Remember to change the application listening port to this in `qiskit_job_manager/server/qiskit_job_manager_server/configure/.env`. In addition, the docker file only maps port 8000. If you change the port, remember to change the port mapping.
5. Build and run docker containers by running (in path `qiskit_job_manager/server/`):
   ```bash
   docker compose up -d
   ```

# Client

## Feature

- [x] Basic APIs for interacting with `qiskit_job_manager_server`.
- [x] Based on [aiohttp](https://github.com/aio-libs/aiohttp) for async operations.

## Set up

1. Install qiskit_job_manager_client package:

   1. Change to the path `qiskit_job_manager/client`:
      ```bash
      cd qiskit_job_manager/cilent
      ```
   2. Install the package by entering the command:
      ```bash
      pip install .
      ```

2. Configure the environment variables:
   1. Change to the path `qiskit_job_manager/client/qiskit_job_manager_client/configure`:
      ```bash
      cd qiskit_job_manager/cilent/qiskit_job_manager_client/configure
      ```
   2. Under the path, copy `.env_example` to `.env` by entering the command:
      ```bash
      cp .env_example .env
      ```
   3. Edit `.env` to change the environment variables.

## Usage

**Notice that many below operations can be async operations when adding `_async` to the end of the class methods**

1. Client initialization

   1. Initialize the object

      ```python
      client = JobManagerClient()
      ```

      or

      ```python
      client = JobManagerClient(host_url = None, host_port = None, email = None, password = None)
      ```

   2. Temporarily change the account
      ```python
      client.login(email = "", password = "")
      ```

2. User-related:

   1. Create a user (ibm_quantum_token is optional when creating the user)
      ```python
      client.create_user(email="", password="", ibm_quantum_token="")
      ```
   2. Print the information of the current login user
      ```python
      client.print_user_info()
      ```
   3. Update the information of the current login user
      ```python
      client.update_user_info(password="", ibm_quantum_token="")
      ```

3. Job-related:

   1. Add jobs

      The input job must be an IBMQJob object.

      To register jobs, the input can be only one job, a list of jobs, or a list of jobs with any dimension.

      ```python
      job = job_1
      job = [job_1, job_2]
      job = [[job_1, job_2], [job_3]]
      ```

      For each job, `notify_status` is a list of [IBMQ job statuses](https://qiskit.org/documentation/stubs/qiskit.providers.JobStatus.html#qiskit.providers.JobStatus) which specify on entering which job status the server will send the email notification.

      `notify_status` is `None` by default, which means only registers "DONE" for every job.

      To specify `notify_status` other than "DONE", `notify_status` must have the same dimension as the input `job`.

      ```python
      client.register_job(job, notify_status=None)
      ```

      One way to quickly register jobs is `using register_start_and_done()`, which registers the first job as "RUNNING" and the last job as "DONE"

      ```python
      client.register_start_and_done(job)
      ```

   2. Print job information

      Print the information of all jobs

      ```python
      client.print_all_job_info()
      ```

      Print the information of a specified IBM job ID. Notice that job_id can also be a list of IDs with any dimension.

      ```python
      client.print_job_info(job_id)
      ```

   3. Update job information

      The input can be a `dict` or a list of `dict`.
      For the information schema, please find [Class JobSchema](qiskit_job_manager/server/qiskit_job_manager_server/schemas/job.py) in job_schema.

      ```python
      client.update_job_info({
           "job_id": "",
           "notify_status": [
               "DONE", "CANCELED"
           ],
      })
      ```

   4. Delete jobs

      Notice that delete jobs only delete the jobs for qiskit_job_manager, so it will do nothing to what you submitted on the IBM Cloud.

      Delete by specifying a list of job IDs with any dimension.

      ```python
      client.delete_job(job_id)
      ```

      Or delete all jobs.

      ```python
      client.delete_all_job()
      ```

## Note for Jupyter Notebook

Due to issues with asyncio in Jupyter Notebook, it may raise the issue **RuntimeError: This event loop is already running in Python**

Fix:
Install `nest_asyncio` and run:

```
import nest_asyncio
nest_asyncio.apply()
```

# License

This project is licensed under the terms of the GNU General Public License v3.0 license.
