from fastapi import FastAPI
import uvicorn
import argparse, multiprocessing, asyncio

from routes.user_routes import user_router
from routes.job_routes import job_router

from notifier.check_job import check_job_status


app = FastAPI()

app.include_router(user_router, tags=["User"], prefix="/user")
app.include_router(job_router, tags=["Job"], prefix="/job")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Qiskit Job Manager!"}


def notify():
    asyncio.run(check_job_status())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help="Host IP", default="127.0.0.1")
    parser.add_argument('--port', type=int, help="Host Port", default=8000)
    args = parser.parse_args()

    notify_process = multiprocessing.Process(target=notify)
    notify_process.start()
    uvicorn.run("main:app", host=args.host, port=args.port, reload=True)

