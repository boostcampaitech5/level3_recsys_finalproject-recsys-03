import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import api, db
from src.exception_handler import add_exception_handler
from src.config import AppConfig

config = AppConfig()

db.connect(
    db=config.db_name,
    host=config.db_host,
    username=config.db_username,
    password=config.db_password,
)

app = FastAPI()
app.include_router(api.router)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
add_exception_handler(app)

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)
