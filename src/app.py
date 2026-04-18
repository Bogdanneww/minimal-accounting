import streamlit as st
import pandas as pd
from collections import defaultdict

from storage import init_db, insert_partner, get_partners, get_journal_data
from engine import (
    post_invoice,
    post_payment,
    post_expense,
    post_vendor_payment
)
from reports import get_pnl, get_partner_ledger
from constants import ACCOUNTS

init_db()

st.set_page_config(layout="wide")

st.title("📊 Minimal Accounting App")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Create Partner",
        "Invoice",
        "Customer Payment",
        "Expense (Create Payable)",
        "Pay Vendor",
        "Reports",
        "Journal"
    ]
)

partners = get_partners()

customers = {f"{p[1]}": p[0] for p in partners if p[2] == "customer"}
vendors = {f"{p[1]}": p[0] for p in partners if p[2] == "vendor"}


# CREATE PARTNER
if menu == "Create Partner":
    name = st.text_input("Name")
    type_ = st.selectbox("Type", ["customer", "vendor"])

    if st.button("Create"):
        insert_partner(name, type_)
        st.success("Created")


# INVOICE
elif menu == "Invoice":
    if not customers:
        st.warning("Create customer first")
    else:
        partner = st.selectbox("Customer", list(customers.keys()))
        amount = st.number_input("Amount", min_value=0.0)

        if st.button("Create Invoice"):
            post_invoice(customers[partner], amount)
            st.success("Invoice posted")


# CUSTOMER PAYMENT
elif menu == "Customer Payment":
    if not customers:
        st.warning("Create customer first")
    else:
        partner = st.selectbox("Customer", list(customers.keys()))
        amount = st.number_input("Amount", min_value=0.0)

        if st.button("Receive Payment"):
            post_payment(customers[partner], amount)
            st.success("Payment posted")


# EXPENSE (AP)
elif menu == "Expense (Create Payable)":
    if not vendors:
        st.warning("Create vendor first")
    else:
        partner = st.selectbox("Vendor", list(vendors.keys()))
        amount = st.number_input("Amount", min_value=0.0)

        if st.button("Record Expense"):
            post_expense(vendors[partner], amount)
            st.success("Expense created (AP)")


# PAY VENDOR
elif menu == "Pay Vendor":
    if not vendors:
        st.warning("Create vendor first")
    else:
        partner = st.selectbox("Vendor", list(vendors.keys()))
        amount = st.number_input("Amount", min_value=0.0)

        if st.button("Pay"):
            post_vendor_payment(vendors[partner], amount)
            st.success("Vendor paid")


# REPORTS
elif menu == "Reports":
    st.subheader("📈 Profit & Loss")

    pnl = get_pnl()

    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue", pnl["Revenue"])
    col2.metric("Expense", pnl["Expense"])
    col3.metric("Profit", pnl["Profit"])

    st.divider()

    st.subheader("👥 Partner Ledger")

    ledger = get_partner_ledger()
    st.dataframe(ledger, use_container_width=True)

    st.caption("""
    Customer (AR): positive → owes you  
    Vendor (AP): negative → you owe vendor
    """)


# JOURNAL
elif menu == "Journal":
    st.subheader("📒 Journal")

    data = get_journal_data()
    grouped = defaultdict(list)

    for row in data:
        tx_id, tx_type, amount, created_at, partner, account, debit, credit = row

        grouped[tx_id].append({
            "type": tx_type,
            "amount": amount,
            "partner": partner,
            "account": account,
            "debit": debit,
            "credit": credit,
        })

    for tx_id, entries in grouped.items():
        st.markdown(f"### Transaction #{tx_id}")

        total_debit = sum(e["debit"] for e in entries)
        total_credit = sum(e["credit"] for e in entries)

        if total_debit == total_credit:
            st.success("Balanced")
        else:
            st.error("NOT Balanced")

        table = []

        for e in entries:
            table.append({
                "Account": f"{e['account']} - {ACCOUNTS[e['account']]}",
                "Debit": e["debit"],
                "Credit": e["credit"],
            })

        st.dataframe(pd.DataFrame(table), use_container_width=True)
        st.divider()
