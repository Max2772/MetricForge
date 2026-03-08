from typing import Dict, Tuple, List, Union

from pydantic import BaseModel


class LB1Response(BaseModel):
    metrics: Dict[str, Union[int, float]]
    operators: List[Tuple[str, int]]
    operands: List[Tuple[str, int]]


class LB2AResponse(BaseModel):
    metrics: Dict[str, Union[int, float]]
    operators: List[Tuple[str, int]]
