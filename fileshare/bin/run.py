import uvicorn
from .settings import get_server_config


def get_workers():
    ...

def start_server():
    conf = get_server_config()
    uvicorn.run(
        app_dir='../fileshare/',
        app='fileshare.main:app', 
        host=conf.HOST, 
        reload=conf.RELOAD, 
        port=conf.PORT
    )