import uuid
from datetime import datetime

from pydantic import BaseModel


class UUIDMixin(BaseModel):
    """Mixin with id field."""

    id: uuid.UUID


class ModifiedMixin(BaseModel):
    """Mixin with modified field."""

    modified: datetime


class PGFilmworkModel(UUIDMixin, ModifiedMixin):
    """A model for movies."""


class PGGenreModel(UUIDMixin, ModifiedMixin):
    """A model for movie genres."""


class PGPersonModel(UUIDMixin, ModifiedMixin):
    """A model for movie personnel."""


class PGGenreFilmworkModel(UUIDMixin, ModifiedMixin):
    """A model for movies by genre."""


class PGPersonFilmworkModel(UUIDMixin, ModifiedMixin):
    """A model for movies with specific persons."""


class ESPersonModel(UUIDMixin):
    """A model for Elasticsearch person instances."""

    name: str | None


class ESGenreAndFilmModel(UUIDMixin):
    name: str


class ESFullPersonModel(UUIDMixin):
    """A model for Elasticsearch full person instances."""

    full_name: str


class ESFilmworkModel(UUIDMixin):
    """A model for Elasticsearch filmwork instances."""

    imdb_rating: float | None
    genres: list[ESGenreAndFilmModel] | None
    title: str
    description: str | None
    directors: list[ESPersonModel] | None
    actors_names: list[str] | None
    writers_names: list[str] | None
    actors: list[ESPersonModel] | None
    writers: list[ESPersonModel] | None


class PGGenreAndFilmModel(UUIDMixin, ModifiedMixin):
    name: str
    description: str | None


class PGPFullersonModel(UUIDMixin, ModifiedMixin):
    """A model for PostgreSQL full person instances."""

    full_name: str
