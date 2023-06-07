import redis


host = "REDIS_HOST"
port = "REDIS_PORT"

redis_app = redis.Redis(host=host, port=port, db=0)
