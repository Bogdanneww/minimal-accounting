import sqlite3
from datetime import datetime

from storage import query, DB_PATH
from constants import TX_CONFIG


def post_transaction(tx_type, partner_id, amount):
    if amount <= 0: return
    p_acc, p_side, o_acc, o_side = TX_CONFIG[tx_type]

    tx_id = query("INSERT INTO transactions (type, partner_id, amount, created_at) VALUES (?, ?, ?, ?)",
                  (tx_type, partner_id, amount, datetime.now().strftime("%Y-%m-%d %H:%M")), commit=True)

    entries = [
        (tx_id, p_acc, amount if p_side == "dr" else 0, amount if p_side == "cr" else 0),
        (tx_id, o_acc, amount if o_side == "dr" else 0, amount if o_side == "cr" else 0)
    ]

    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany("INSERT INTO entries (transaction_id, account, debit, credit) VALUES (?, ?, ?, ?)", entries)
