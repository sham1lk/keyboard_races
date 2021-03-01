from requests import get
from coolname import generate_slug

import redis
Redis = redis.Redis(host='localhost', port=6379, db=0)


def get_ip():
    return get('https://api.ipify.org').text


def get_name():
    try:
        if not Redis.get('name'):
            Redis.set('name', generate_slug(2))
        return Redis.get('name')
    except redis.ConnectionError:
        print("Redis is not setup. Contact administrator")
    return generate_slug(2)
