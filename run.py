import subprocess

from ui import start_app
import sqlite3
# subprocess.Popen(['celery', '-A', 'tasks', 'worker' '--concurrency=1'],
#                      stdout=subprocess.PIPE,
#                      stderr=subprocess.PIPE)
conn = sqlite3.connect('orders.db')
cur = conn.cursor()
cur.execute("""DROP table IF EXISTS users;""")
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   name TEXT PRIMARY KEY,
   room TEXT,
   progres INT);
""")
conn.commit()
start_app()
