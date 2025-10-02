from fastapi import FastAPI
from bytebox_apps.master.routers import execution

app = FastAPI()

app.include_router(execution.router)