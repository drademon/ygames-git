from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class Operation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime = None
    type: str


class OperationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    data: List[Operation]
    details: str

#    class Config:
#        orm_mode = True
