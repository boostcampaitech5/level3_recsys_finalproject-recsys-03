import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.router import root_router
from src.log.ExceptionHandler import add_exception_handler
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()
app.include_router(root_router.router)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
add_exception_handler(app)

if __name__ == "__main__":
    uvicorn.run(app, host=os.environ["HOST"], port=int(os.environ["PORT"]))