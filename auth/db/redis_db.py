import redis

from auth.utils.settings import settings


host = settings.REDIS_HOST
port = settings.REDIS_PORT

redis_app = redis.Redis(host=host, port=port, db=0)
