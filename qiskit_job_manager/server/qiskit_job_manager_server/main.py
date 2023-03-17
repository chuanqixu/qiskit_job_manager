import uvicorn
import argparse, multiprocessing, asyncio
from .backend.configure import settings
from .backend.notifier.check_job import check_job_status

def notify():
    asyncio.run(check_job_status())

def run(host=settings.HOST, port=settings.PORT, **kwargs):
    uvicorn.run("qiskit_job_manager_server.backend.app:app", host=host, port=port, **kwargs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help="Host IP", default=settings.HOST)
    parser.add_argument('--port', type=int, help="Host Port", default=settings.PORT)
    args = parser.parse_args()

    notify_process = multiprocessing.Process(target=notify)
    notify_process.start()
    uvicorn.run("qiskit_job_manager_server.backend.app:app", host=args.host, port=args.port, reload=True, log_level="info")
