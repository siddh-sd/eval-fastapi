import redis
from config import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD


async def redis_client():
	redis_client = redis.Redis(
		host=REDIS_HOST,
		port=REDIS_PORT,
		password=REDIS_PASSWORD,
		decode_responses=True  
	)
	return redis_client