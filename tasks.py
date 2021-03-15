import sqlite3

import celery
from celery.worker.control import Panel

from kombu import Queue, Exchange
from kombu.common import Broadcast

from helpers import get_name

conn = sqlite3.connect('orders.db')
cur = conn.cursor()

app = celery.Celery('example')
#REDIS_URL = "redis://:GgEiVNGLaSd82TQ0Zv0F4t49OC5XQsWw@redis-10176.c238.us-central1-2.gce.cloud.redislabs.com:10176"
app.conf.broker_url = "amqp://xekacxtl:c2GI0ApaiIIgnVuSumk3ZogdsEUAkedK@jellyfish.rmq.cloudamqp.com/xekacxtl"
#app.conf.result_backend = "amqp://xekacxtl:c2GI0ApaiIIgnVuSumk3ZogdsEUAkedK@jellyfish.rmq.cloudamqp.com/xekacxtl"pip install kombu
app.conf.task_default_queue = 'broadcast_tasks'
app.conf.task_queues = (Broadcast('broadcast_tasks'),)

@app.task()
def send_progress(name, progres):
    cur.execute(
        """REPLACE INTO users (name, progres) VALUES(?, ?);""", (name,
                                                                progres))
    conn.commit()
