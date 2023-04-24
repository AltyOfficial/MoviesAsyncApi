from elasticsearch import Elasticsearch
from utils.index_settings import create_es_index
import os
from dotenv import load_dotenv
from pg_extractor import PostgresExtractor
import psycopg2
from psycopg2.extras import DictCursor
from es_loader import ESLoader

load_dotenv()

es = Elasticsearch(hosts='http://localhost:9200/')

BLOCK_SIZE = 500

INDEX_NAME = 'person_index'

dsl = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
}


def run(extractor: PostgresExtractor, loader: ESLoader):
    """Extracting data from postgres and loading to ES."""

    for data in extractor.extract_data():

        loader.load(data, INDEX_NAME)

        # break

        # try:
        #     print(len(data))
        # except Exception:
        #     print('error')



if __name__ == '__main__':

    if not es.indices.exists(index=INDEX_NAME):
        create_es_index(es, INDEX_NAME)
    
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:

        extractor = PostgresExtractor(pg_conn, BLOCK_SIZE)
        loader = ESLoader(es)

        run(extractor, loader)

    # if not es.indices.exists(index=INDEX_NAME):
    #     create_es_index(es, INDEX_NAME)
