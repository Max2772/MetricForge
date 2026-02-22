from pydantic import BaseModel
from typing import Dict, Union


class FirstLBResponse(BaseModel):
    metrics: Dict[str, Union[int, float]]
    operators: Dict[str, int]
    operands: Dict[str, int]