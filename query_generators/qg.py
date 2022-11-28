from api.request import Request


class QueryGenerator:
    _request: Request

    def __init__(self, request: Request):
        self._request = request

    def generate_query(self):
        query = {
            "query": {
                "bool": {
                    "must": [{"match": {"Category": self._request.Category}},
                             {"match": {"Operation_Mode": self._request.Operation_Mode}},
                             {"range": {"Hourly_Rate": {'gte': self._request.Hourly_Rate_Min}}},
                             {"range": {"Hourly_Rate": {'lte': self._request.Hourly_Rate_Max}}}],
                    "filter": {
                        "term": {
                            "Notice_Period": self._request.Notice_Period
                        }
                    }
                }
            }
        }
        return query
