import sqlite3

conn = sqlite3.connect("flashchallenger.db")

def init_db():
    conn.execute(
        "CREATE TABLE IF NOT EXISTS challenges ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "text TEXT NOT NULL, "
        "category TEXT NOT NULL)"
    )
    conn.commit()

def random_challenge(used=()):
    marks = ",".join("?" * len(used))
    sql = f"SELECT id, text FROM challenges WHERE id NOT IN ({marks}) ORDER BY RANDOM() LIMIT 1"
    return conn.execute(sql, tuple(used)).fetchone()