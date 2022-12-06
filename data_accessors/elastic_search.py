from elasticsearch import Elasticsearch
from config import Environment
import pandas as pd
import json

env = Environment()


class MainDataAccessor:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MainDataAccessor, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Create client and insert data
        self._instance = self.create_index()

    def to_bulk_json(self,input_df):
        """Converts dataframe to bulk json format"""
        bulk_actions = []
        for record in input_df.to_dict(orient="records"):
            bulk_actions.append(('{ "index" : { "_index" : "%s" }}' % env.ES_INDEX))
            bulk_actions.append(json.dumps(record, default=int))
        return bulk_actions

    def create_index(self):

        # Create the client instance
        client = Elasticsearch(hosts="http://localhost:9200", verify_certs=False)
        # Successful response!
        print("Successfully connected to index at: ", env.ES_URL)

        print("Reading data from data frame... ")
        df = pd.read_csv(env.CSV_FILE_PATH)

        print("Converting dataframe to bulk jsons.... ")
        bulk_json_object = self.to_bulk_json(df)

        print("Ingesting bulk json object into Elastic Search index:", env.ES_INDEX)
        client.bulk(index=env.ES_INDEX, operations=bulk_json_object)
        print("Successfully resume json objects into Elastic Search:", env.ES_INDEX)

        return client

