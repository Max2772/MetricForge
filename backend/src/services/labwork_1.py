from fastapi import HTTPException

from ..logger import logger
from ..utils.halstead import HalsteadFS
from ..models.responses import LB1Response
from ..models.requests import LabRequest


analyzer = HalsteadFS()

async def get_labwork1_response(input_data: LabRequest) -> LB1Response:
    try:
        metrics, operators, operands = analyzer.calculate(
            code=input_data.code,
            string_as_operand=input_data.string_as_operand,
        )
    except Exception as e:
        logger.error(f"Внутренняя ошибка сервера в labwork/1: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

    return LB1Response(
        metrics=metrics,
        operators=operators,
        operands=operands
    )