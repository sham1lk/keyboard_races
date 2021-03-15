from helpers import get_name
from ui import start_app
import celery
import sqlite3
conn = sqlite3.connect('orders.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   name TEXT PRIMARY KEY,
   progres INT);
""")

conn.commit()
start_app()
