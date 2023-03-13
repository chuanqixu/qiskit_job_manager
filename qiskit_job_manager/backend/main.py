from fastapi import FastAPI
import uvicorn
import argparse

app = FastAPI()

@app.get("/")
def read_root():
    return {"messasge": "Welcome to Qiskit Job Manager!"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help="Host IP", default="127.0.0.1")
    parser.add_argument('--port', type=int, help="Host Port", default=8000)

    args = parser.parse_args()

    uvicorn.run("main:app", host=args.host, port=args.port, reload=True)
