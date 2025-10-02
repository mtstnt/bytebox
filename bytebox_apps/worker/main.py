from docker import DockerClient
from fastapi import FastAPI

def main():
    client = DockerClient.from_env()
    print(client.images.list())

if __name__ == "__main__":
    main()