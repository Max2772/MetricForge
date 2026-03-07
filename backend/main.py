import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.env import LOG_LEVEL, API_HOST, API_PORT, API_RELOAD
from src.logger import logger
from src.models.requests import LabRequest
from src.services import (get_labwork1_response, get_labwork2A_response)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lab_handlers = {
    "1": get_labwork1_response,
    "2A": get_labwork2A_response,
    "2B": ...,
    "3": ...,
}


@app.get("/")
async def index():
    return {"message": "Nothing here, look docs"}


@app.post("/labwork/{lab_id}")
async def labwork_endpoint(lab_id: str, input_data: LabRequest):
    handler = lab_handlers.get(lab_id.upper())
    if not handler:
        raise HTTPException(status_code=404, detail="Некорректный lab_id")
    return await handler(input_data)


if __name__ == '__main__':
    logger.info("Запуск FastAPI сервера...")

    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_RELOAD,
        log_level=LOG_LEVEL.lower(),
        access_log=True
    )
