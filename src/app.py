import streamlit as st
import pandas as pd
from collections import defaultdict

from storage import init_db, insert_partner, get_partners, get_journal_data
from engine import post_invoice, post_payment, post_expense
from reports import get_pnl, get_partner_ledger
from constants import ACCOUNTS

init_db()

st.title("Minimal Accounting App")

menu = st.sidebar.selectbox(
    "Menu",
    ["Create Partner", "Invoice", "Payment", "Expense", "Reports", "Journal"]
)

partners = get_partners()
partner_dict = {f"{p[1]} ({p[2]})": p[0] for p in partners}


if menu == "Create Partner":
    name = st.text_input("Name")
    type_ = st.selectbox("Type", ["customer", "vendor"])

    if st.button("Create"):
        insert_partner(name, type_)
        st.success("Partner created")


elif menu == "Invoice":
    if not partner_dict:
        st.warning("Create a partner first")
    else:
        partner = st.selectbox("Customer", list(partner_dict.keys()))
        amount = st.number_input("Amount", min_value=0.0)

        if st.button("Create Invoice"):
            post_invoice(partner_dict[partner], amount)
            st.success("Invoice posted")


elif menu == "Payment":
    if not partner_dict:
        st.warning("Create a partner first")
    else:
        partner = st.selectbox("Customer", list(partner_dict.keys()))
        amount = st.number_input("Amount", min_value=0.0)

        if st.button("Register Payment"):
            post_payment(partner_dict[partner], amount)
            st.success("Payment posted")


elif menu == "Expense":
    if not partner_dict:
        st.warning("Create a partner first")
    else:
        partner = st.selectbox("Vendor", list(partner_dict.keys()))
        amount = st.number_input("Amount", min_value=0.0)

        if st.button("Record Expense"):
            post_expense(partner_dict[partner], amount)
            st.success("Expense recorded")


elif menu == "Reports":
    st.subheader("Profit & Loss")
    pnl = get_pnl()
    st.write(pnl)

    st.subheader("Partner Ledger")
    ledger = get_partner_ledger()
    st.dataframe(ledger)


elif menu == "Journal":
    st.subheader("Journal Entries")

    data = get_journal_data()

    grouped = defaultdict(list)

    for row in data:
        tx_id, tx_type, amount, partner, account, debit, credit = row
        grouped[tx_id].append({
            "type": tx_type,
            "amount": amount,
            "partner": partner,
            "account": account,
            "debit": debit,
            "credit": credit
        })

    for tx_id, entries in grouped.items():
        first = entries[0]

        st.markdown(f"""
        ### Transaction #{tx_id}
        - Type: **{first['type']}**
        - Partner: **{first['partner']}**
        - Amount: **{first['amount']}**
        """)

        table_data = []
        for e in entries:
            acc_name = ACCOUNTS.get(e["account"], e["account"])

            table_data.append({
                "Account": f"{e['account']} - {acc_name}",
                "Debit": e["debit"],
                "Credit": e["credit"]
            })

        df = pd.DataFrame(table_data)
        st.table(df)

        st.divider()
