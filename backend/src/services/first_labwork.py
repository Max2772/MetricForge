from fastapi import HTTPException

from ..logger import logger
from ..utils.halstead import HalsteadFS
from ..models.responses import FirstLBResponse
from ..models.requests import FirstLBRequest


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