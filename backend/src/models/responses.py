from pydantic import BaseModel
from typing import Dict, Tuple, List, Union


class FirstLBResponse(BaseModel):
    metrics: Dict[str, Union[int, float]]
    operators: List[Tuple[str, int]]
    operands: List[Tuple[str, int]]