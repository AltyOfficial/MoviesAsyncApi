import logging

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1 import films, genres, persons
from core.config import settings
from core.logger import LOGGING
from db import elastic, redis

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


# Return 400 BAD_REQUEST instead of 422 HTTP_UNPROCESSABLE_ENTITY
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


@app.on_event('startup')
async def startup():
    redis.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    elastic.es = AsyncElasticsearch(
        hosts=[
            f'{settings.ELASTIC_SCHEME}://'
            f'{settings.ELASTIC_HOST}'
            f':{settings.ELASTIC_PORT}'
        ]
    )


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


# Подключаем роутер к серверу, указав префикс /v1/films
# Теги указываем для удобства навигации по документации
app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
