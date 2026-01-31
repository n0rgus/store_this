# db.py
from __future__ import annotations
import sqlite3
from flask import g, current_app

def get_db() -> sqlite3.Connection:
    """Get a SQLite connection bound to this request context."""
    if "db" not in g:
        db_path = current_app.config["STORE_THIS_DB"]
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def q_all(sql: str, params: tuple = ()):
    cur = get_db().execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return rows

def q_one(sql: str, params: tuple = ()):
    cur = get_db().execute(sql, params)
    row = cur.fetchone()
    cur.close()
    return row

def exec_sql(sql: str, params: tuple = ()):
    db = get_db()
    cur = db.execute(sql, params)
    db.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id

def init_app(app):
    @app.teardown_appcontext
    def close_db(exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()
