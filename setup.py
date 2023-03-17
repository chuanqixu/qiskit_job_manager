from setuptools import setup, find_packages
import os

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

server_path = os.path.join(os.path.dirname(__file__), "qiskit_job_manager", "server")
client_path = os.path.join(os.path.dirname(__file__), "qiskit_job_manager", "client")

setup(name='qiskit_job_manager',
    version='0.0.1',
    description='Qiskit Job Manager',
    author='Chuanqi Xu',
    author_email='chuanqi.xu@yale.edu',
    #   url='https://www.python.org/sigs/distutils-sig/',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'server': [f'qiskit_job_manager_server @ file://{server_path}'],
        'client': [f'qiskit_job_manager_client @ file://{client_path}'],
    },
)
