import uvicorn
import psutil
import os

from .settings import get_server_config


def get_workers():
    if os.environ.get('stage') is 'LOCAL':
        return 1 
    else:
        cores = psutil.cpu_count(logical = True)
        return 2*cores+1


def start_server():
    conf = get_server_config()
    uvicorn.run(
        app_dir='../fileshare/',
        app='fileshare.main:app', 
        host=conf.HOST, 
        reload=conf.RELOAD, 
        port=conf.PORT,
        workers=get_workers()
    )