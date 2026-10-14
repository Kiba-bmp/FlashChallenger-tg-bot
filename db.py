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

def random_challenge(exclude_id=0):
    sql = "SELECT id, text FROM challenges WHERE id != ? ORDER BY RANDOM() LIMIT 1"
    return conn.execute(sql, (exclude_id,)).fetchone()