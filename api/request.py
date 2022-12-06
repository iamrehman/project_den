from pydantic import BaseModel


class Request(BaseModel):
    Category: str
    Hourly_Rate_Min: int
    Hourly_Rate_Max: int
    Operation_Mode: int
    Notice_Period: int
    rerank_using_ml_model: bool


class ModelRequest(BaseModel):
    model: str
    parameters: dict


