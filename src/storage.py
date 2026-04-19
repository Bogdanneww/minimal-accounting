import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "accounting.db"


def query(sql, params=(), commit=False, fetch=False):
    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(sql, params)
        if commit:
            conn.commit()
        return cur.fetchall() if fetch else cur.lastrowid


def init_db():
    query(
        "CREATE TABLE IF NOT EXISTS partners (id INTEGER PRIMARY KEY, name TEXT, type TEXT)",
        commit=True,
    )
    query(
        "CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, type TEXT, partner_id INTEGER, amount REAL, created_at TEXT)",
        commit=True,
    )
    query(
        "CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, transaction_id INTEGER, account TEXT, debit REAL, credit REAL)",
        commit=True,
    )


def get_journal_data():
    return query(
        """
        SELECT t.id, t.type, t.amount, t.created_at, p.name, e.account, e.debit, e.credit
        FROM transactions t JOIN partners p ON t.partner_id = p.id JOIN entries e ON e.transaction_id = t.id
        ORDER BY t.id DESC, e.id ASC""",
        fetch=True,
    )
