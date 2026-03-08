from fastapi import HTTPException

from ..logger import logger
from ..utils.glib import GilbFS
from ..models.responses import LB2AResponse
from ..models.requests import LabRequest


analyzer = GilbFS()

async def get_labwork2A_response(input_data: LabRequest) -> LB2AResponse:
    try:
        metrics, operators = analyzer.calculate(
            code=input_data.code,
        )
    except Exception as e:
        logger.error(f"Внутренняя ошибка сервера в labwork/2A: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

    return LB2AResponse(
        metrics=metrics,
        operators=operators,
    )