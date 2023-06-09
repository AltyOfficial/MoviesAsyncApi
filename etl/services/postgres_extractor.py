import psycopg2
import datetime
from dotenv import load_dotenv
from psycopg2 import OperationalError
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor

from etl.utils import models_validation, queries
from etl.utils.backoff_decorator import backoff
from etl.utils.etl_logging import logger
from etl.utils.settings import etl_settings, pg_settings

load_dotenv()


class PostgresConnector:
    """Connects to PostgreSQL database."""

    def __init__(self, settings=pg_settings):
        self.dsn: dict = {
            'dbname': settings.POSTGRES_DB,
            'user': settings.POSTGRES_USER,
            'password': settings.POSTGRES_PASSWORD,
            # 'dbname': settings.DB_NAME,
            # 'user': settings.DB_USER,
            # 'password': settings.DB_PASSWORD,
            'host': settings.DB_HOST,
            'port': settings.DB_PORT,
            'options': settings.DB_OPTIONS
        }
        self.conn: connection | None

    def connect(self) -> connection:
        return psycopg2.connect(**self.dsn, cursor_factory=DictCursor)


class PostgresExtractor:
    """Performs extract functions of data."""

    def __init__(self):
        self.state: etl_settings.STATE
        self.conn: connection = self.connect_to_pg()

    @backoff(exception=OperationalError)
    def connect_to_pg(self) -> connection:
        """Connection to PostgreSQL database."""

        logger.info('Connecting to PostgreSQL...')

        with PostgresConnector().connect() as conn:
            logger.info('Connected to PostgreSQL.')
            return conn

    def close(self) -> None:
        """Closes PostgreSQL connection."""

        if self.conn:
            self.conn.close()
            logger.info('Connection to PostgreSQL closed.')

    def execute_query(self, query: str):
        """Execute a query to PostgreSQL database and return a result."""

        with self.conn.cursor() as curs:
            curs.execute(query)
            return curs.fetchall()

    def fetch_modified_genres(self, timestamp: datetime) -> list:
        """Return a list with movies' genres modified or added anew."""

        genres = self.execute_query(
            query=queries.get_modified_genres(timestamp=timestamp)
        )

        if genres:
            return [
                models_validation.PGGenreModel(**genre)
                for genre in genres
            ]

        return []

    def fetch_filmworks_by_modified_genres(self, genres: list[str]) -> list:
        """Return movies if corresponding genres have been modified."""

        filmworks = self.execute_query(
            query=queries.get_modified_filmworks_by_genres(genres=genres)
        )

        return [
            models_validation.PGGenreFilmworkModel(
                **filmwork
            ).id for filmwork in filmworks
        ]

    def fetch_modified_persons(self, timestamp: datetime) -> list:
        """Return a list with movies' personnel modified or added anew."""

        persons = self.execute_query(
            query=queries.get_modified_persons(timestamp=timestamp)
        )

        if persons:
            return [
                models_validation.PGPersonModel(**person)
                for person in persons
            ]

        return []

    def fetch_filmworks_by_modified_persons(self, persons: list[str]) -> list:
        """Return movies if corresponding personnel has been modified."""

        filmworks = self.execute_query(
            query=queries.get_modified_filmworks_by_persons(persons=persons)
        )

        return [
            models_validation.PGPersonFilmworkModel(
                **filmwork
            ).id for filmwork in filmworks
        ]

    def fetch_modified_filmworks(self, timestamp: datetime) -> list:
        """Return a list with movies modified or added anew."""

        filmworks = self.execute_query(
            query=queries.get_modified_filmworks(timestamp=timestamp)
        )

        if filmworks:
            return [
                models_validation.PGFilmworkModel(**filmwork)
                for filmwork in filmworks
            ]

        return []

    def fetch_filmworks_by_id(self, ids: tuple) -> list[tuple] | None:
        """Return movies' instances."""

        if ids:
            return self.execute_query(
                query=queries.get_filmwork_by_id(ids=ids)
            )

        return None

    def fetch_persons(self, timestamp: datetime) -> list:
        """Return a list with persons data."""

        persons = self.execute_query(
            query=queries.get_persons(timestamp=timestamp)
        )

        if persons:
            return [
                models_validation.PGPFullersonModel(**person).dict()
                for person in persons
            ]

        return []

    def fetch_genres_with_films(self, timestamp: datetime) -> list[tuple]:
        """Return genres' instances."""

        genres = self.execute_query(
            query=queries.get_genres(timestamp=timestamp)
        )

        if genres:
            return [
                models_validation.PGGenreAndFilmModel(**genre).dict()
                for genre in genres
            ]

        return []
