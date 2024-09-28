from func.functions import *
from fastapi import FastAPI
import asyncio, uvicorn
from models.orm import *
from routers.routs import router

from config import BACKEND_PORT, BACKEND_HOST

app = FastAPI()

app.include_router(router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI with APIRouter!"}

#starting FastAPI
if __name__ == '__main__':
    create_tables()
    uvicorn.run("main:app", reload=True, host=BACKEND_HOST, port=int(BACKEND_PORT))





