import pandas as pd
import sqlite3
from storage import DB_PATH


def get_report_df(sql):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(sql, conn)


def get_pnl():
    df = get_report_df("SELECT account, debit, credit FROM entries")
    if df.empty:
        return {"Revenue": 0, "Expense": 0, "Profit": 0}
    rev = df[df["account"] == "4000"]["credit"].sum()
    exp = df[df["account"] == "5000"]["debit"].sum()
    return {"Revenue": rev, "Expense": exp, "Profit": rev - exp}


def get_account_balance(acc_code):
    df = get_report_df(
        f"SELECT debit, credit FROM entries WHERE account = '{acc_code}'"
    )
    if df.empty:
        return 0.0

    if acc_code in ["1000", "1100", "5000"]:
        return df["debit"].sum() - df["credit"].sum()
    else:
        return df["credit"].sum() - df["debit"].sum()


def get_cash_balance():
    return get_account_balance("1000")


def get_partner_ledger():
    df = get_report_df("""
                       SELECT p.name as "Partner", p.type as "Type", e.account, e.debit, e.credit
                       FROM entries e
                                JOIN transactions t ON e.transaction_id = t.id
                                JOIN partners p ON t.partner_id = p.id
                       WHERE e.account IN ('1100', '2000')""")

    if df.empty:
        return pd.DataFrame()

    def calc_balance(r):
        if r["account"] == "1100":
            return r["debit"] - r["credit"]
        else:  # Account 2000
            return r["debit"] - r["credit"]

    df["Balance"] = df.apply(calc_balance, axis=1)
    summary = df.groupby(["Partner", "Type"])["Balance"].sum().reset_index()
    return summary
