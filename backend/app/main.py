from fastapi import FastAPI, Depends, HTTPException
from fastapi import FastAPI

from app.api.api import api_router

app = FastAPI()

app.include_router(api_router)