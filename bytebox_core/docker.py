import os
from docker import DockerClient

def list_images():
    client = DockerClient.from_env()
    return client.images.list()