from fastapi import HTTPException

from backend.src.logger import logger
from backend.src.utils.halstead import HalsteadFS
from backend.src.models.responses import FirstLBResponse
from backend.src.models.requests import FirstLBRequest


async def get_first_labwork_response(input_data: FirstLBRequest) -> FirstLBResponse:
    try:
        analyzer = HalsteadFS()
        metrics, operators, operands = analyzer.calculate(input_data.code)
    except Exception as e:
        logger.error(f"Unexpected error in labwork/1: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

    return FirstLBResponse(
        metrics=metrics,
        operators=operators,
        operands=operands
    )