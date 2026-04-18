from storage import insert_transaction, insert_entries


def post_invoice(partner_id, amount):
    tx_id = insert_transaction("invoice", partner_id, amount)

    entries = [
        (tx_id, "1100", amount, 0),  # DR Accounts Receivable
        (tx_id, "4000", 0, amount),  # CR Revenue
    ]

    insert_entries(entries)


def post_payment(partner_id, amount):
    tx_id = insert_transaction("payment", partner_id, amount)

    entries = [
        (tx_id, "1000", amount, 0),  # DR Cash
        (tx_id, "1100", 0, amount),  # CR Accounts Receivable
    ]

    insert_entries(entries)


def post_expense(partner_id, amount):
    tx_id = insert_transaction("expense", partner_id, amount)

    entries = [
        (tx_id, "5000", amount, 0),  # DR Expense
        (tx_id, "1000", 0, amount),  # CR Cash
    ]

    insert_entries(entries)
