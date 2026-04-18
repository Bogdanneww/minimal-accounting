import pandas as pd
from storage import get_entries


def get_pnl():
    data = get_entries()
    df = pd.DataFrame(data, columns=["account", "debit", "credit", "partner_id"])

    revenue = df[df["account"] == "4000"]["credit"].sum()
    expense = df[df["account"] == "5000"]["debit"].sum()

    return {
        "Revenue": revenue,
        "Expense": expense,
        "Profit": revenue - expense,
    }


def get_partner_ledger():
    data = get_entries()
    df = pd.DataFrame(data, columns=["account", "debit", "credit", "partner_id"])

    df["balance"] = df["debit"] - df["credit"]

    ledger = df.groupby("partner_id")["balance"].sum().reset_index()

    return ledger
