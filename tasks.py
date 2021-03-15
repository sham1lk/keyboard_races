import sqlite3

import celery
from kombu import Queue, Exchange
from kombu.common import Broadcast

from helpers import get_name

conn = sqlite3.connect('orders.db')
cur = conn.cursor()

app = celery.Celery('example')
REDIS_URL = "redis://:GgEiVNGLaSd82TQ0Zv0F4t49OC5XQsWw@redis-10176.c238.us-central1-2.gce.cloud.redislabs.com:10176"
app.conf.broker_url = REDIS_URL
app.conf.result_backend = REDIS_URL


@app.task()
def add():
    return "123"


@app.task()
def celery_get_name():
    return 'hi'


@app.task()
def send_progress(name, progres):
    cur.execute(
        """REPLACE INTO users (name, progres) VALUES(?, ?);""", (name,
                                                                progres))
    conn.commit()
