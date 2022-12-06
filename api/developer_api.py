import pandas as pd
from fastapi import APIRouter, Depends
from .request import Request
import config

from elasticsearch.helpers import scan

from query_generators.qg import QueryGenerator

router = APIRouter()


@router.get(
    "/get_applicants",
    summary="Get applicants"
)
def get_applicants(request: Request):
    """Hello world api"""
    qg = QueryGenerator(request)
    query = qg.generate_query()
    client = config.client
    rel = scan(client=client._instance,
               query=query,
               index='resume',
               raise_on_error=True,
               preserve_order=True,
               clear_scroll=True)
    # Keep response in a list.
    result = list(rel)
    temp = []
    for hit in result:
        temp.append(hit['_source'])
    # Create a dataframe.
    df = pd.DataFrame(temp)
    df = df.set_index("Applicant_ID")
    output = df.to_dict()
    output.pop('Unnamed: 0')
    return df.to_dict()
