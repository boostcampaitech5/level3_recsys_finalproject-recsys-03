import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import api, db
from src.exception_handler import add_exception_handler
from dotenv import load_dotenv

load_dotenv(".env")

db.connect(
    db=os.environ.get("DB_HOST"),
    host=os.environ.get("DB_NAME"),
    username=os.environ.get("DB_USERNAME"),
    password=os.environ.get("DB_PASSWORD"),
)

app = FastAPI()
app.include_router(api.router)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
add_exception_handler(app)

if __name__ == "__main__":
    uvicorn.run(app, host=os.environ["HOST"], port=int(os.environ["PORT"]))
