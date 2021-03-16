
import sqlite3
from datetime import datetime

from coolname import generate_slug

conn = sqlite3.connect('orders.db')
cur = conn.cursor()

sample_text = [
    "In some natures there are no half-tones;\nnothing but raw primary colours. John Bodman\nwas a man who was always at one extreme or the other",
    "When and where, it matters not now to\nrelate--but once upon a time as I was\npassing through a thinly peopled district\nof country, night came down upon me, almost unawares.",
    "Some women had risen, in order to get\nnearer to him, and were standing with their\neyes fastened on the clean-shaven face\nof the judge, who was saying such weighty things",
    "Conradin hated her with a desperate sincerity\nwhich he was perfectly able to mask.",
    "The man held a double-barrelled gun cocked in his\nhand, and screwed up his eyes in the direction\nof his lean old dog who was running on ahead sniffing the bushes"
]

def get_name():
    return generate_slug(2)


def get_progres(name):
    try:
        cur.execute("SELECT progres FROM users where name=?", (name,))
        return int(cur.fetchall()[0][0])
    except:
        return 0


def get_players(name):
    cur.execute("SELECT room FROM users where name=?", (name,))
    game = cur.fetchall()
    if game:
        cur.execute("SELECT name FROM users where room=? order by name",
                    (game[0][0],))
    return cur.fetchall()


def get_game(name):
    cur.execute("SELECT room FROM users where name=?", (name,))
    game = cur.fetchall()
    if game:
        cur.execute("SELECT * FROM game where name=?", (game[0][0],))
        return cur.fetchall()
    else:
        return False


def string_to_time(str):
    return datetime.strptime(str, '%Y-%m-%d %H:%M:%S.%f')
