from pydantic import BaseModel


class Applicant(BaseModel):
    Applicant_ID: str = "32421"
    Resume: str = "Cool Applicant."


class Response(BaseModel):
    applicants: list = []
