import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.env import LOG_LEVEL, API_HOST, API_PORT, API_RELOAD
from src.logger import logger
from src.services.halstead import HalsteadFS
from src.models.responses import LabworkResponse


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def index():
    return {'Nothing here, look docs'}

@app.post("/labwork/{lab_id}")
def analyze_lab(lab_id: int, input_data: LabworkResponse):
    if lab_id != input_data.labwork_id:
        raise HTTPException(status_code=400, detail="lab_id в URL не совпадает с labwork_id в теле")

    if lab_id != 1:
        return {"status": "Не готово", "lab_id": lab_id}

    analyzer = HalsteadFS()
    metrics, operators, operands = analyzer.calculate(input_data.code)

    return {
        "lab_id": lab_id,
        "metrics": metrics,
        "operators": operators,
        "operands": operands
    }


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
