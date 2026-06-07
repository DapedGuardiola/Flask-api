from dotenv import load_dotenv
import redis
import os
load_dotenv()

r = redis.Redis(
    host = os.getenv('REDIS_HOST','localhost'),
    port = int(os.getenv('REDIS_PORT','6379')),
    password = os.getenv('REDIS_PASSWORD',None),
    db = 0,
    protocol = 2
)