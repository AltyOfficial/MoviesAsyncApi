from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    es_genre_index: str = 'test_genres'
    es_id_field: str = 'id'
    es_index_mapping: dict = {}

    redis_host: str = Field('http://127.0.0.1:6379', env='REDIS_HOST')
    service_url: str = Field('http://127.0.0.1:8000/api/v1/', env='SERVICE_URL')
 

test_settings = TestSettings()