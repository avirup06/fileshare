from fastapi import FastAPI
import os

from fileshare.api.login_registration_routes import router as login_router
from fileshare.api.profile_routes import router as profile_router
from fileshare.api.file_routes import router as file_router
from fileshare.db import Base, engine


app = FastAPI(
    title="File Share Backend",
    description="Welcome to File Share Backend - API documentation!",
    docs_url="/docs",
    openapi_url="/docs/openapi.json"
)


@app.on_event("startup")
async def startup_db(): 
   Base.metadata.create_all(bind=engine)


app.include_router(login_router, tags=['signup and login'])
app.include_router(profile_router, prefix='/user', tags=['profile'])
app.include_router(file_router, prefix='/files', tags=['file'])


@app.get("/")
async def root():
    return {"message": "File Share Backend"}

