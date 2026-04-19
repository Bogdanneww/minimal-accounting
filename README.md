# 💰 Minimal Accounting System

A lightweight, robust accounting system based on the **Double-Entry Bookkeeping** principle. Built with **Python**, **Streamlit**, and **SQLite**, this application provides a clear financial overview for small projects or freelancers.

---

## 🚀 Key Features
* **Double-Entry Ledger:** Every transaction automatically creates balanced Debit and Credit entries, ensuring data integrity.
* **Financial Dashboard:** Real-time visualization of Account Balances, Accounts Receivable (AR), Accounts Payable (AP), and Net Profit.
* **Partner Management:** Dedicated tracking for both Customers and Vendors.
* **General Journal:** A transparent, auditable history of all accounting records.
* **Containerized:** Fully Dockerized for consistent deployment across any environment.

---

## 📁 Project Structure
```text
minimal-accounting/
├── data/               # Persistent SQLite database storage
├── src/                # Source code directory
│   ├── app.py          # Streamlit UI & Entry point
│   ├── constants.py    # Chart of Accounts & App constants
│   ├── engine.py       # Accounting logic (Transaction processing)
│   ├── reports.py      # Business intelligence (PnL, Balances)
│   └── storage.py      # Database layer (SQL execution)
├── .dockerignore       # Prevents local bloat from entering Docker images
├── .gitignore          # Standard Git exclusions
├── Dockerfile          # Multi-stage build configuration
├── requirements.txt    # Python dependencies
├── PROMPT_HISTORY.md   # History of prompts
└── README.md           # Documentation
```
---

## 🛠 Installation & Setup

You can run this project using Docker (Recommended) or locally in a Python environment.

## 🛠 Clone the repository
```bash
git clone https://github.com/Bogdanneww/minimal-accounting.git
cd minimal-accounting
```

## 🛠 Installation (Local)

### 1️⃣ Create virtual environment
```bash 
python -m venv .venv
```

### Windows
```bash
.venv\Scripts\activate
```

### macOS/Linux
```bash
source .venv/bin/activate
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### Run application
```bash
streamlit run src/app.py
```

### Open in browser:
👉 http://localhost:8501/


### 🐳 Run with Docker
```bash
docker build -t minimal-accounting .
docker run -p 8501:8501 -v "${PWD}/data:/app/data" minimal-accounting
```

### Open in browser:
👉 http://localhost:8501/

### 📊 Reports
Profit & Loss (P&L) — Revenue, Expenses, Net Profit

Partner Ledger — balances for customers and vendors

Balance Sheet (simplified) — overview of all accounts

General Journal — grouped accounting entries

### 📘 Chart of Accounts
1000 — Cash

1100 — Accounts Receivable

2000 — Accounts Payable

4000 — Revenue

5000 — Expense

### 👨‍💻 Author

Bohdan Mykyichuk
