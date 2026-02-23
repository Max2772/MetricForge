from pydantic import BaseModel


class FirstLBRequest(BaseModel):
    code: str
    string_as_operand: bool = False

