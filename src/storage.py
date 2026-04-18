import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "accounting.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS partners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        type TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        partner_id INTEGER,
        amount REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id INTEGER,
        account TEXT,
        debit REAL,
        credit REAL
    )
    """)

    conn.commit()
    conn.close()


def insert_partner(name, type_):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO partners (name, type) VALUES (?, ?)", (name, type_))
    conn.commit()
    conn.close()


def get_partners():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, type FROM partners")
    data = cur.fetchall()
    conn.close()
    return data


def insert_transaction(type_, partner_id, amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (type, partner_id, amount) VALUES (?, ?, ?)",
        (type_, partner_id, amount),
    )
    tx_id = cur.lastrowid
    conn.commit()
    conn.close()
    return tx_id


def insert_entries(entries):
    conn = get_connection()
    cur = conn.cursor()
    cur.executemany(
        "INSERT INTO entries (transaction_id, account, debit, credit) VALUES (?, ?, ?, ?)",
        entries,
    )
    conn.commit()
    conn.close()


def get_entries():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.account, e.debit, e.credit, t.partner_id
        FROM entries e
        LEFT JOIN transactions t ON e.transaction_id = t.id
    """)
    data = cur.fetchall()
    conn.close()
    return data


def get_journal_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            t.id,
            t.type,
            t.amount,
            p.name,
            e.account,
            e.debit,
            e.credit
        FROM transactions t
        LEFT JOIN partners p ON t.partner_id = p.id
        LEFT JOIN entries e ON e.transaction_id = t.id
        ORDER BY t.id
    """)

    data = cur.fetchall()
    conn.close()
    return data
