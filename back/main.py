import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.router import root_router
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()
app.include_router(root_router.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credendials = True,
    allow_methods = ["*"],
    allow_headers=["*"]
)


if __name__ == "__main__":
    uvicorn.run(app, host=os.environ["HOST"], port=int(os.environ["PORT"]))
