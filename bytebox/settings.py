import sys
# Disable bytecode generation
sys.dont_write_bytecode = True

import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./bytebox.db")
DOCKER_HOST = os.environ.get("DOCKER_HOST", "unix:///var/run/docker.sock")

AUTH_ENABLED = os.environ.get("AUTH_ENABLED", "false") == "true"
JWT_SECRET = os.environ.get("JWT_SECRET", "secretsecretsecretsecretsecretsecretsecretsecretsecretsecret")