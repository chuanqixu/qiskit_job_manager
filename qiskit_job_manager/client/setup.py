from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='qiskit_job_manager_client',
    version='0.0.1',
    description='Qiskit Job Manager Client',
    author='Chuanqi Xu',
    author_email='chuanqi.xu@yale.edu',
    #   url='https://www.python.org/sigs/distutils-sig/',
    packages=find_packages(),
    install_requires=requirements,
)
