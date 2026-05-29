import sqlite3
from utils.db import DB_PATH, get_conn


def check_login(username: str, password: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT username, role, full_name FROM users WHERE username=? AND password=?",
        (username, password)
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None
