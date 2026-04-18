import pandas as pd
from storage import get_connection


def get_pnl():
    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT account, debit, credit
        FROM entries
    """, conn)

    conn.close()

    revenue = df[df["account"] == "4000"]["credit"].sum()
    expense = df[df["account"] == "5000"]["debit"].sum()

    return {
        "Revenue": revenue,
        "Expense": expense,
        "Profit": revenue - expense,
    }


# PARTNER LEDGER
def get_partner_ledger():
    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT 
            p.name as partner,
            p.type as type,
            e.account,
            e.debit,
            e.credit
        FROM entries e
        LEFT JOIN transactions t ON e.transaction_id = t.id
        LEFT JOIN partners p ON t.partner_id = p.id
    """, conn)

    conn.close()

    df["balance"] = df["debit"] - df["credit"]

    # AR (1100) → клієнт винен нам
    # AP (2000) → ми винні постачальнику
    result = df[df["account"].isin(["1100", "2000"])]

    ledger = result.groupby(["partner", "type"])["balance"].sum().reset_index()

    return ledger
