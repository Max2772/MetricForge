from pydantic import BaseModel


class FirstLBRequest(BaseModel):
    code: str

