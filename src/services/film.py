import json
from functools import lru_cache
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.config import settings
from db.elastic import AsyncSearchAbstract, elastic, get_elastic
from db.redis import AsyncCacheAbstract, get_redis, redis
from models.models import FilmFull, FilmShort
from redis.asyncio import Redis


FILM_CACHE_EXPIRE_IN_SECONDS = settings.REDIS_CACHE_EXPIRES_IN_SECONDS
INDEX_NAME = settings.ES_MOVIE_INDEX


class ElasticService(AsyncSearchAbstract):
    """Class to represent search engine with ElasticSearch."""

    def __init__(self, elastic: AsyncElasticsearch, index_name: str):
        self.elastic = elastic
        self.index_name = index_name

    async def _get_single_object(self, film_id: str) -> FilmFull | None:
        """Retrieve a film instance from Elasticsearch DB."""

        try:
            doc = await self.elastic.get(index=self.index_name, id=film_id)
        except NotFoundError:
            return None
        return FilmFull(**doc['_source'])

    async def _get_list_of_objects(
        self,
        search_query: dict
    ) -> tuple[int, list[FilmShort]]:
        """Return a list of movies from Elasticsearch DB with a paginator."""

        result = await self.elastic.search(
            index=self.index_name,
            body=search_query
        )
        total = result['hits']['total']['value']
        hits = result['hits']['hits']

        if not hits:
            return total, []

        try:
            films = [hits[i]['_source'] for i in range(search_query['size'])]
        except IndexError:
            films = [hit['_source'] for hit in hits]

        return total, [FilmShort(**film) for film in films]


class RedisService(AsyncCacheAbstract):
    """Class to represent cache service with Redis."""

    def __init__(self, redis: Redis):
        self.redis = redis

    async def _get_single_object(self, film_id: str) -> FilmFull | None:
        """Retrieve a film instance from Redis cache. """

        cache_key = f'film:{film_id}'
        data = await self.redis.get(cache_key)

        if not data:
            return None

        return FilmFull.parse_raw(data)

    async def _get_list_of_objects(
        self,
        page: int,
        size: int,
        query: str = None,
        genre: UUID = None
    ) -> tuple[int, list[FilmShort]]:
        """Retrieve films from Redis cache. """

        cache_key = f'films:{page}:{size}:{query}:{genre}'
        data = await self.redis.get(cache_key)

        if not data:
            return 0, None

        films_data = json.loads(data)
        films = [FilmShort.parse_raw(film) for film in films_data['films']]
        total = films_data['total']

        return total, films

    async def _put_single_object(self, film: FilmFull):
        """Save a film instance to Redis cache."""

        cache_key = f'film:{str(film.id)}'

        await self.redis.set(
            cache_key,
            film.json(),
            FILM_CACHE_EXPIRE_IN_SECONDS
        )

    async def _put_list_of_objects(
        self,
        page: int,
        size: int,
        total: int,
        films: list[FilmShort],
        query: str = None,
        genre: UUID = None
    ) -> None:
        """Save films to Redis cache."""

        cache_key = f'films:{page}:{size}:{query}:{genre}'
        data = {
            'total': total,
            'films': [film.json() for film in films]
        }
        json_str = json.dumps(data)

        await self.redis.set(
            cache_key, json_str, FILM_CACHE_EXPIRE_IN_SECONDS
        )


cache_service = RedisService(redis)
search_service = ElasticService(elastic, INDEX_NAME)


class FilmService:
    """Class to represent films logic."""

    def __init__(
        self,
        redis: AsyncCacheAbstract,
        elastic_search: AsyncSearchAbstract,
        index_name: str
    ) -> None:
        self.redis_service = redis
        self.es_service = elastic_search
        self.index_name = index_name

    async def get_films(
        self,
        page: int,
        size: int,
        genre: UUID
    ) -> tuple[int, list[FilmShort]]:
        """
        Retrieve films instances to list films
        in accordance with filtration conditions.
        """

        total, films = await cache_service._get_list_of_objects(
            page, size, genre
        )

        if not films:
            start_index = (page - 1) * size

            if not genre:
                search_query = {
                    "query": {"match_all": {}},
                    "sort": [{"imdb_rating": {"order": "desc"}}],
                    "from": start_index,
                    "size": size
                }
            else:
                search_query = {
                    "query": {
                        "nested": {
                            "path": "genres",
                            "query": {
                                "bool": {
                                    "filter": [
                                        {
                                            "term": {"genres.id": genre}
                                        }
                                    ]
                                }
                            }
                        }
                    },
                    "sort": [{"imdb_rating": {"order": "desc"}}],
                    "from": start_index,
                    "size": size
                }

            total, films = await search_service._get_list_of_objects(
                search_query
            )

            if not films:
                return 0, None

            await cache_service._put_list_of_objects(
                page, size, total, films, genre
            )

            return total, films

        return total, films

    async def search_films(
        self,
        page: int,
        size: int,
        query: str
    ) -> tuple[int, list[FilmShort]]:
        """
        Retrieve films instances to list films
        in accordance with search conditions.
        """

        total, films = await cache_service._get_list_of_objects(
            page, size, query
        )

        if not films:
            start_index = (page - 1) * size
            search_query = {
                "query": {"match": {"title": query}},
                "sort": [
                    {"_score": {"order": "desc"}},
                    {"imdb_rating": {"order": "desc"}},
                ],
                "from": start_index,
                "size": size
            }

            total, films = await search_service._get_list_of_objects(
                search_query
            )

            if not films:
                return 0, None

            await cache_service._put_list_of_objects(
                page, size, total, films, query
            )

            return total, films

        return total, films

    async def get_by_id(self, film_id: str) -> FilmFull | None:
        """Return a film instance in accordance with ID given."""

        film = await cache_service._get_single_object(film_id)

        if not film:
            film = await search_service._get_single_object(film_id)

            if not film:
                return None

            await cache_service._put_single_object(film)

        return film


@lru_cache()
def get_film_service(
        redis: RedisService = Depends(get_redis),
        elastic: ElasticService = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic, INDEX_NAME)
