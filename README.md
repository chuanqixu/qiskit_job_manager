# qiskit_job_manager

## Server

### Feature

* [X] Basic APIs for IBM Quantum job management based on [FastAPI](https://github.com/tiangolo/fastapi), including sending emails when job status meets the requirements.
* [X] Ready-to-use register, login, reset passwords, and authentication based on [FastAPI Users](https://github.com/fastapi-users/fastapi-users#readme).

### Usage

1. Install qiskit_job_manager_server package:
   1. Change to the path `qiskit_job_manager/server`.
   2. Install the package by entering the command:
        ```shellscript
            $ pip install .
        ```
2. Configure the environment variables:
   1. Change to the path `qiskit_job_manager/server/qiskit_job_manager_server/configure`
   2. Under the path, copy `.env_example` to `.env` by entering the command:
        ```shellscript
            $ cp .env_example .env
        ```
   3. Edit `.env` to change the environment variables.
3. Start the server by choosing one of the ways:
   1. Directly run the main file by entering the command:
        ```shellscript
            python qiskit_job_manager/server/qiskit_job_manager_server/main.py
        ```
   2. Run the code with the main function:
        ```python
            from qiskit_job_manager_server import run_server

            run_server()
        ```

## Client

### Feature



### Usage

1. Install qiskit_job_manager_client package:
   1. Change to the path `qiskit_job_manager/client`.
   2. Install the package by entering the command:
        ```shellscript
            $ pip install .
        ```
