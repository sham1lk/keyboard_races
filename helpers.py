from requests import get
from coolname import generate_slug

import redis
Redis = redis.Redis(host='localhost', port=6379, db=0)


def get_ip():
    return get('https://api.ipify.org').text


def get_name():
    return generate_slug(2)
