ACCOUNTS = {
    "1000": "Cash",
    "1100": "Accounts Receivable",
    "2000": "Accounts Payable",
    "4000": "Revenue",
    "5000": "Expense",
}

TX_CONFIG = {
    "invoice": ("1100", "dr", "4000", "cr"),
    "payment": ("1100", "cr", "1000", "dr"),
    "expense": ("2000", "cr", "5000", "dr"),
    "vendor_payment": ("2000", "dr", "1000", "cr"),
}
