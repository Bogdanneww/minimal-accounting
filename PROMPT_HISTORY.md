# 📝 Detailed Prompt History — Minimal Accounting Web App

This document provides a comprehensive log of the iterative development process. It tracks the evolution of the project from initial domain research to final deployment optimization, highlighting the collaboration between the developer and AI.

---

## 1. Requirement Analysis & Constraint Mapping
**Prompt:**
"I am starting a Python test task: 'Minimal Accounting Web App'. Help me deconstruct the requirements. Identify the 'non-negotiable' technical constraints and define what 'success' looks like for a reviewer who values pragmatism over feature-creep."

**Outcome:**
Identified that a working Dockerfile is a hard requirement. Success is defined by a balanced double-entry logic (DR=CR), a clean UI using Streamlit, and a focused reporting layer (P&L and Partner Ledger) without the complexity of a full ERP.

---

## 2. Accounting Domain: The Logic of Double-Entry
**Prompt:**
"Explain the core mechanics of double-entry accounting in a way that can be translated into a database schema. Focus on how Assets, Liabilities, Equity, Revenue, and Expenses interact via Debits and Credits."

**Outcome:**
Understood the fundamental equation: Assets = Liabilities + Equity. Established that for every business event, the sum of debits must equal the sum of credits. This formed the basis for the validation logic in the posting engine.

---

## 3. Designing the Minimal Data Model
**Prompt:**
"Propose a SQLite schema for a minimal accounting system. I need to track Partners (Customers/Vendors), Transactions (the business event), and Journal Entries (the actual accounting lines). Keep it simple but ensure referential integrity."

**Outcome:**
Created a 3-table structure: `partners`, `transactions` (metadata like date and description), and `journal_entries` (linked to transactions and accounts with separate DR/CR or signed amount columns).

---

## 4. Chart of Accounts (COA) Definition
**Prompt:**
"The task requires a fixed chart of accounts. Define the exact codes for Cash, Accounts Receivable, Accounts Payable, Revenue, and Expense. How should these codes be structured to make reporting easier?"

**Outcome:**
Standardized on: 1000 (Cash), 1100 (AR), 2000 (AP), 4000 (Revenue), 5000 (Expense). This numeric structure allows for easy filtering: codes starting with 1-3 go to the Balance Sheet, while 4-5 go to the P&L.

---

## 5. Layered Architecture Selection
**Prompt:**
"I want to avoid 'spaghetti code' in my Streamlit app. Suggest a project structure that separates the database logic, business accounting rules, and the UI components. I'm using Python 3.11."

**Outcome:**
Adopted a modular structure: `storage.py` (SQL), `engine.py` (Accounting logic), `reports.py` (Aggregations), and `app.py` (Streamlit UI). This ensures that accounting logic can be tested independently of the web interface.

---

## 6. Development of the Posting Engine
**Prompt:**
"Write a Python class for the 'Accounting Engine'. It should have methods like `post_invoice` and `post_payment`. For each method, specify which accounts are debited and credited. Include a check to ensure DR - CR = 0."

**Outcome:**
Implemented the core business logic. For example, an Invoice debits 1100 (AR) and credits 4000 (Revenue). A Payment debits 1000 (Cash) and credits 1100 (AR).

---

## 7. Business Event Modeling (UX perspective)
**Prompt:**
"What are the 4 most critical business events for a small service-based business that will demonstrate the full flow of AR and AP? I need to build UI forms for these."

**Outcome:**
Selected: 1. Sales Invoice (Customer), 2. Receiving Payment (Customer), 3. Recording Expense (Vendor), 4. Paying Vendor. This covers both revenue and expense cycles.

---

## 8. Streamlit Navigation & Tab Structure
**Prompt:**
"Design a clean navigation flow in Streamlit. I want a Sidebar for main categories: Dashboard, Transactions, and Reports. How can I manage 'session state' to ensure the UI updates after a transaction is posted?"

**Outcome:**
Built a multi-tab/sidebar system using `st.sidebar.selectbox`. Used `st.rerun()` to refresh the UI and clear input forms after successful database commits.

---

## 9. Dashboard & Financial Metrics
**Prompt:**
"I need a 'High-Level' dashboard. Calculate and display 4 key metrics using Streamlit's `st.metric`: Current Cash, Total AR, Total AP, and Net Profit. Use colors to indicate 'good' or 'bad' status (e.g., high AP in red)."

**Outcome:**
Created a visual summary that provides immediate financial health insight, meeting the 'Product Goal' of the task.

---

## 10. General Journal Visualization
**Prompt:**
"How should I display the General Journal in Streamlit so it looks like a professional accounting ledger? I need to group entries by transaction ID and show DR/CR columns clearly."

**Outcome:**
Implemented a grouped view using Pandas styling. Added transaction descriptions and partner names to the rows to improve auditability.

---

## 11. Reporting Logic: Profit & Loss (P&L)
**Prompt:**
"Write a function in `reports.py` that calculates the P&L. It should sum all entries for account 4000 and 5000, then subtract them. How do I handle the fact that Revenue has a natural Credit balance in the database?"

**Outcome:**
Refined the reporting logic to correctly interpret account signs. Developed a clean table showing Total Revenue, Total Expenses, and the resulting Net Profit.

---

## 12. Partner Ledger Implementation
**Prompt:**
"Design a report that shows the balance for each partner. If it's a Customer, it should show how much they owe me (AR). If it's a Vendor, how much I owe them (AP)."

**Outcome:**
Created the Partner Ledger report. It aggregates entries by `partner_id` for specific accounts (1100/2000), allowing the user to click a partner and see their transaction history.

---

## 13. Data Validation & Edge Cases
**Prompt:**
"What happens if a user tries to submit an empty transaction or a negative amount? Add validation layers to the UI and the Engine to prevent 'dirty' data from hitting the SQLite file."

**Outcome:**
Added `st.error` alerts for invalid inputs and `try-except` blocks in the engine to handle database constraints, ensuring the app doesn't crash on user error.

---

## 14. Refactoring: Eliminating Redundant Code
**Prompt:**
"I noticed I'm writing the same SQL query for getting account balances in three different places. Help me refactor this into a reusable helper function in `storage.py`."

**Outcome:**
Improved code maintainability by centralizing data access. Created `get_balance(account_code)` and `get_partner_balance(partner_id)`.

---

## 15. SQL Join Optimization (Debugging)
**Prompt:**
"My journal view is missing the Partner names; it only shows IDs. Fix the SQL query to JOIN the `journal_entries` with `partners` and `transactions` tables without creating duplicate rows."

**Outcome:**
Optimized the reporting queries to provide human-readable names across all views, enhancing the "Reviewability" of the app.

---

## 16. Streamlit Visual Polish
**Prompt:**
"The app looks a bit plain. Suggest some Streamlit 'hacks' to improve the UX. Maybe use `st.expander` for transaction details or `st.dataframe` with custom column widths."

**Outcome:**
Enhanced the UI using expanders for the Journal and adding tooltips to explain what each account code (e.g., 1000, 1100) represents.

---

## 17. Accounting Correctness Audit
**Prompt:**
"Double-check my posting logic. If I record a Vendor Expense for $100, I should Debit 5000 and Credit 2000. Is this correct for a double-entry system? Does it correctly affect the P&L and the Partner Ledger?"

**Outcome:**
Verified that the logic is sound. Expense (5000) increases on Debit (lowering P&L), and AP (2000) increases on Credit (increasing debt to vendor).

---

## 18. Preparing for Containerization
**Prompt:**
"I need to wrap this in Docker. I'm using SQLite, which is a file. How can I ensure the database isn't deleted every time the container restarts? Explain the concept of Docker Volumes for this specific case."

**Outcome:**
Learned the importance of mounting a local directory to `/app/data` inside the container to ensure data persistence across builds and restarts.

---

## 19. Writing a Professional Dockerfile
**Prompt:**
"Provide a Dockerfile for a Python 3.11-slim image. It should be optimized for size and build speed (use layer caching for requirements). It must expose port 8501 for Streamlit."

**Outcome:**
Received a high-quality Dockerfile that separates dependency installation from code copying, resulting in much faster rebuilds during development.

---

## 20. Creating a .dockerignore Strategy
**Prompt:**
"What files should I exclude from my Docker image? I have a `.venv`, `__pycache__`, and a local `.git` folder. Provide a `.dockerignore` file that keeps the image clean."

**Outcome:**
Minimized image size and avoided security risks by excluding virtual environments, local databases, and IDE configuration files.

---

## 21. Documentation: Crafting the README
**Prompt:**
"Write a professional README.md in English. It should include a clear project structure, installation steps for both local and Docker users, and a short explanation of the technical decisions (like why SQLite and Streamlit were used)."

**Outcome:**
Produced a comprehensive guide that makes the project easy to start and review, fulfilling the 'Working Delivery' success criteria.

---

## 22. Code Cleanup & Import Optimization
**Prompt:**
"Review my `storage.py` and `app.py`. I have some unused imports and inconsistent variable naming. Help me clean this up to meet the 'Code and Structure' evaluation criteria."

**Outcome:**
Refactored the code for better readability. Removed redundant `import os` and `import sys` calls and standardized on `snake_case` for all variables.

---

## 23. Final Docker Build & Run Test
**Prompt:**
"I just ran `docker build` and it took 80 seconds. Is this normal? Also, help me write the exact `docker run` command with the volume flag for my D:\ drive path."

**Outcome:**
Confirmed the build was successful. Verified that the volume mapping `${PWD}/data:/app/data` correctly persisted the `accounting.db` file on the host machine.

---

## 24. Convergence Check against Task Goals
**Prompt:**
"Let's review the 'Success Signs' from the task description. Do we have a Partner Ledger? Yes. Do we have a P&L? Yes. Is the COA fixed? Yes. Is there any unnecessary complexity we should remove?"

**Outcome:**
Decided to remove a planned 'Currency Converter' feature to stay pragmatic and focused on the core accounting flow as requested in the 'Scope Guidance'.

---

## 25. Final Polish & Deployment Prep
**Prompt:**
"I'm ready to push to GitHub. Give me a checklist of what to double-check in my public repository to ensure I don't fail the 'Acceptance Conditions'."

**Outcome:**
Verified the presence of: 1. Source code, 2. Dockerfile, 3. README, 4. Prompt History. Confirmed the repo is public and the instructions are clear for the reviewer.
