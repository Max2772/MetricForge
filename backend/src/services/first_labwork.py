from fastapi import HTTPException

from ..logger import logger
from ..utils.halstead import HalsteadFS
from ..models.responses import FirstLBResponse
from ..models.requests import FirstLBRequest


analyzer = HalsteadFS()

async def get_first_labwork_response(input_data: FirstLBRequest) -> FirstLBResponse:
    try:
        metrics, operators, operands = analyzer.calculate(
            code=input_data.code,
            string_as_operand=input_data.string_as_operand,
        )
    except Exception as e:
        logger.error(f"Внутренняя ошибка сервера в labwork/1: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

    return FirstLBResponse(
        metrics=metrics,
        operators=operators,
        operands=operands
    )