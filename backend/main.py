import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.services.first_labwork import get_first_labwork_response
from src.env import LOG_LEVEL, API_HOST, API_PORT, API_RELOAD
from src.logger import logger
from src.models.requests import FirstLBRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return {"message": "Nothing here, look docs"}

@app.post("/labwork/1")
async def first_labwork_endpoint(input_data: FirstLBRequest):
    return await get_first_labwork_response(input_data)


if __name__ == '__main__':
    logger.info("Staring FastAPI server...")

    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_RELOAD,
        log_level=LOG_LEVEL.lower(),
        access_log=True
    )
