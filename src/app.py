import streamlit as st
import pandas as pd
from storage import init_db, query, get_journal_data
from engine import post_transaction
from reports import get_pnl, get_partner_ledger, get_account_balance, get_cash_balance
from constants import ACCOUNTS

init_db()
st.set_page_config(page_title="Minimal Accounting", page_icon="💰", layout="wide")

# Main title
st.title("🏦 Minimal Accounting System")
st.caption("Professional Double-Entry Ledger")
st.divider()

# Sidebar navigation
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    st.divider()
    menu = st.radio(
        "Menu",
        ["🤝 Partners", "💸 Transactions", "🏠 Dashboard", "📖 General Journal"],
        label_visibility="collapsed"
    )

# Obtaining partner data
partners = query("SELECT id, name, type FROM partners", fetch=True)
p_map = {f"{p[1]} ({p[2]})": (p[0], p[2]) for p in partners}

# --- PARTNERS ---
if menu == "🤝 Partners":
    st.subheader("🤝 Partner Management")
    with st.expander("➕ Add New Partner", expanded=not bool(partners)):
        c1, c2 = st.columns(2)
        name = c1.text_input("Name / Company Name")
        p_type = c2.selectbox("Relationship", ["customer", "vendor"])
        if st.button("Save Partner"):
            if name.strip():
                query("INSERT INTO partners (name, type) VALUES (?, ?)", (name, p_type), commit=True)
                st.success(f"✅ Partner '{name}' created successfully!")
                st.rerun()
            else:
                st.error("Partner name cannot be empty.")

    if partners:
        st.write("### Active Partners")
        df_p = pd.DataFrame(partners, columns=["ID", "Name", "Type"])
        st.dataframe(df_p, use_container_width=True, hide_index=True)

# --- TRANSACTIONS ---
elif menu == "💸 Transactions":
    st.subheader("📝 Post New Transaction")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            type_options = [
                ("invoice", "📄 Customer Invoice"),
                ("payment", "💰 Receive Payment"),
                ("expense", "🧾 Vendor Bill"),
                ("vendor_payment", "💸 Pay Vendor")
            ]
            type_select = st.selectbox("Operation", type_options, format_func=lambda x: x[1])
        with c2:
            p_options = list(p_map.keys())
            if p_options:
                p_label = st.selectbox("Partner", p_options)
                amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, format="%.2f")
            else:
                st.warning("Please create a partner first in the 'Partners' tab.")

        if p_options and st.button("🚀 Post Transaction", use_container_width=True):
            if amount > 0:
                post_transaction(type_select[0], p_map[p_label][0], amount)
                st.success(f"✅ Success! Transaction for {p_label} recorded: ${amount:,.2f}")
            else:
                st.error("Amount must be greater than zero.")

# --- DASHBOARD ---
elif menu == "🏠 Dashboard":
    pnl = get_pnl()
    cash = get_account_balance("1000")
    ar = get_account_balance("1100")
    ap = get_account_balance("2000")

    # First row: 5 main accounts
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("💰 Cash (1000)", f"${cash:,.2f}")
    m2.metric("⏳ Receivable (1100)", f"${ar:,.2f}")
    m3.metric("🧾 Payable (2000)", f"${ap:,.2f}")
    m4.metric("📈 Revenue (4000)", f"${pnl['Revenue']:,.2f}")
    m5.metric("📉 Expenses (5000)", f"${pnl['Expense']:,.2f}")

    st.write("")

    # Dedicated block for Net Profit
    with st.container(border=True):
        col_text, col_val = st.columns([3, 1])
        with col_text:
            st.markdown("### 💎 Net Profit ")
            st.caption("Financial result for the current period (Revenue - Expenses)")
        with col_val:
            profit = pnl['Profit']
            color = "#2e7d32" if profit >= 0 else "#d32f2f"
            st.markdown(f"<h2 style='text-align: right; color: {color};'>${profit:,.2f}</h2>", unsafe_allow_html=True)

    st.divider()

    # Full-width partner table
    st.subheader("👥 Partner Balances")
    ledger = get_partner_ledger()
    if not ledger.empty:
        def style_bal(val):
            color = 'red' if val < 0 else 'green' if val > 0 else 'grey'
            return f'color: {color}; font-weight: bold'


        st.dataframe(
            ledger.style.map(style_bal, subset=['Balance']).format({"Balance": "${:,.2f}"}),
            use_container_width=True, hide_index=True
        )
    else:
        st.info("No partner data available.")

# --- JOURNAL ---
elif menu == "📖 General Journal":
    st.subheader("📖 General Journal")
    data = get_journal_data()
    if data:
        df_j = pd.DataFrame(data, columns=["ID", "Type", "Total", "Date", "Partner", "Acc", "Debit", "Credit"])
        st.dataframe(
            df_j.style.format({"Debit": "{:,.2f}", "Credit": "{:,.2f}", "Total": "{:,.2f}"}),
            use_container_width=True, hide_index=True
        )
    else:
        st.info("The journal is empty.")
