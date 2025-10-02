import os
import sys

# Disable bytecode generation
sys.dont_write_bytecode = True

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./bytebox.db")
DOCKER_HOST = os.environ.get("DOCKER_HOST", "unix:///var/run/docker.sock")