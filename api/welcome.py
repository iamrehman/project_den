from fastapi import APIRouter, Depends
from .response import Response

router = APIRouter()


@router.get(
    "/",
    summary="Hello World",
    response_model=Response,
)
def hello_world():
    """Hello world api"""
    return Response()


