import sys
# Disable bytecode generation
sys.dont_write_bytecode = True

from fastapi import FastAPI
from bytebox.auth import api as auth
from bytebox.sandbox import api as sandbox
from bytebox.users import api as users
from bytebox.workers import api as workers
from bytebox.pipelines import api as pipelines

app = FastAPI()

app.mount('/api/v1', app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(sandbox.router)
app.include_router(workers.router)
app.include_router(pipelines.router)