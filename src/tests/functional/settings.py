from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://localhost:9200')
    redis_host: str = Field('localhost')
    redis_port: str = Field(6379)
    service_url: str = Field('http://localhost:8000/api/v1/')
    es_movie_index: str = 'movies'
    es_person_index: str = 'persons'
    es_genre_index: str = 'genres'
    es_id_field: str = 'id'


test_settings = TestSettings()
