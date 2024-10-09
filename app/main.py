# main.py
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from .routers import auth  
app = FastAPI()

app.include_router(auth.router)


