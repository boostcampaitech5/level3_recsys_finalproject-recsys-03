import uvicorn
import os
from fastapi import FastAPI
from src.router import root_router
from src.log import ExceptionHandler
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()
app.include_router(root_router.router)
ExceptionHandler.add_exception_handler(app)

if __name__ == "__main__":
    uvicorn.run(app, host=os.environ["HOST"], port=int(os.environ["PORT"]))
