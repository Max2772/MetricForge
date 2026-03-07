from typing import Optional

from pydantic import BaseModel


class LabRequest(BaseModel):
    code: str = None
    string_as_operand: Optional[bool] = None
