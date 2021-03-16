import sqlite3

import celery

from kombu.common import Broadcast


conn = sqlite3.connect('orders.db')
cur = conn.cursor()

app = celery.Celery('example')
app.conf.broker_url = "amqp://xekacxtl:c2GI0ApaiIIgnVuSumk3ZogdsEUAkedK@jellyfish.rmq.cloudamqp.com/xekacxtl"
app.conf.task_default_queue = 'broadcast_tasks'
app.conf.task_queues = (Broadcast('broadcast_tasks'),)


@app.task()
def send_progress(name, room, progres):
    cur.execute(
        """REPLACE INTO users (name, room, progres) VALUES(?, ?, ?);""", (name,
                                                                room, progres))
    conn.commit()


@app.task()
def pregame_communication(name, text, time):
    cur.execute(
        """REPLACE INTO game (name, text, time) VALUES(?, ?, ?);""", (name,
                                                                text, time))
    conn.commit()
