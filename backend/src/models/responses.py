from pydantic import BaseModel


class LabworkResponse(BaseModel):
    labwork_id: int
    code: str