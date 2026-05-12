# Law-Firm
A law firm for managing lawyers, judges, assigning cases , reports
# ⚖️ Law Firm Management System

A full-stack database management system for law firms, built with **Python**, **Streamlit**, **SQL Server**, and **PyODBC**. Developed as a Database Systems Lab project at FAST-NUCES (Spring 2026).

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-2019+-CC2927?logo=microsoftsqlserver&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Modules](#modules)
- [SQL & Stored Procedures](#sql--stored-procedures)
- [Validation](#validation)
- [Screenshots](#screenshots)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Authors](#authors)

---

## Overview

The **Law Firm Management System** digitizes the daily record-keeping operations of a law firm. It replaces error-prone manual methods with a structured relational database backed by a clean, interactive web UI.

**Problems it solves:**
- Duplicate or lost records
- Slow case/client lookups
- Disorganized evidence and payment tracking
- No centralized view of case timelines

---

## Features

- ✅ Full **CRUD** operations across all modules
- 🔍 Search records by ID or filters
- 📊 Live dashboard with record counts
- 🔐 Input validation (email, CNIC, phone, date, amount)
- ⚙️ Stored procedures for secure, reusable DB operations
- 🧾 Case-Lawyer assignment tracking
- 📅 Hearing timeline management
- 📝 Lawyer journal notes per case
- 💳 Payment status tracking

---

## Tech Stack

| Technology | Role |
|---|---|
| Python 3.10+ | Backend logic |
| Streamlit | Web UI / frontend |
| SQL Server 2019+ | Relational database |
| SSMS | Query development & testing |
| T-SQL | Queries and stored procedures |
| PyODBC | Python ↔ SQL Server connection |

---

## Database Schema

The database consists of **9 relational tables**:

```
Judge ──────────────────────────────┐
Client ─────────────────────────────┤
                                    ▼
                              ┌───────────┐
                              │   Case    │
                              └─────┬─────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            ▼                       ▼                        ▼
       Case_Lawyer              Timeline                  Evidence
            │
            ▼
         Lawyer
            │
            ▼
         Journal

Payment ──────── linked to Case, Client, Lawyer
```

### Tables

| Table | Description |
|---|---|
| `Judge` | Court judges |
| `Client` | Law firm clients |
| `Lawyer` | Lawyers with specialization & bar number |
| `Case` | Legal cases (title, type, status, filing date) |
| `Case_Lawyer` | Many-to-many: lawyers assigned to cases |
| `Timeline` | Hearing dates, proceedings, outcomes |
| `Journal` | Lawyer notes per case |
| `Evidence` | Evidence linked to cases |
| `Payment` | Payment records (amount, date, status) |

---

## Project Structure

```
law-firm-management-system/
│
├── app/
│   ├── main.py                  # Streamlit entry point
│   ├── db_connection.py         # PyODBC connection setup
│   │
│   ├── modules/
│   │   ├── judge.py
│   │   ├── client.py
│   │   ├── lawyer.py
│   │   ├── case.py
│   │   ├── case_lawyer.py
│   │   ├── timeline.py
│   │   ├── journal.py
│   │   ├── evidence.py
│   │   └── payment.py
│   │
│   └── utils/
│       └── validators.py        # Input validation helpers
│
├── sql/
│   ├── schema.sql               # Table creation scripts
│   ├── stored_procedures.sql    # All stored procedures
│   └── sample_data.sql          # Sample records for testing
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Microsoft SQL Server (2019+ recommended)
- SQL Server Management Studio (SSMS) — optional but helpful
- ODBC Driver 17 or 18 for SQL Server

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/law-firm-management-system.git
cd law-firm-management-system
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt`**
```
streamlit
pyodbc
python-dotenv
```

### 3. Set Up the Database

Open SSMS and run the scripts in order:

```sql
-- 1. Create tables
source sql/schema.sql

-- 2. Create stored procedures
source sql/stored_procedures.sql

-- 3. (Optional) Insert sample data
source sql/sample_data.sql
```

### 4. Configure the Connection

Copy `.env.example` to `.env` and fill in your SQL Server details:

```env
DB_SERVER=localhost
DB_NAME=LawFirmDB
DB_DRIVER=ODBC Driver 17 for SQL Server
# Leave blank to use Windows Authentication:
DB_USERNAME=
DB_PASSWORD=
```

### 5. Run the App

```bash
streamlit run app/main.py
```

The app will open at `http://localhost:8501`.

---

## Modules

### 🧑‍⚖️ Judge Module
Manage court judges — add, view, search by ID, update, and delete.

### 👤 Client Module
Store client details: name, CNIC, address, phone, email.

### 👨‍💼 Lawyer Module
Track lawyers with specialization, bar number, contact info, and hourly rates.

### 📁 Case Module
Manage legal cases with titles, types, statuses, and filing dates. Cases require a valid Client ID and Judge ID.

### 🔗 Case-Lawyer Assignment
Link one or more lawyers to a case. Supports role designation (e.g., Lead Lawyer, Advisor).

### 📅 Timeline Module
Record hearing dates, next hearing dates, proceedings, and outcomes for each case.

### 📓 Journal Module
Lawyers can add notes per case. The lawyer must be assigned to the case beforehand.

### 🔍 Evidence Module
Store evidence titles, types, descriptions, and file paths per case.

### 💰 Payment Module
Track payments linked to cases — amount, date, and status (Paid / Pending). Supports quick status updates.

---

## SQL & Stored Procedures

### Example Queries

```sql
-- Get all judges
SELECT * FROM Judge;

-- Find a specific client
SELECT * FROM Client WHERE Client_id = 1;

-- Close a case
UPDATE [Case]
SET Status = 'Closed'
WHERE Case_id = 101;

-- Remove a payment
DELETE FROM Payment
WHERE Payment_id = 5;
```

### Stored Procedures

| Procedure | Action |
|---|---|
| `add_judge` | Insert a new judge |
| `update_client` | Update client details |
| `add_case` | Add a new legal case |
| `delete_payment` | Remove a payment record |
| `get_all_cases` | Retrieve all cases |

Stored procedures improve **security**, reduce **code duplication**, and boost **query performance**.

---

## Validation

The system validates all user input before writing to the database:

| Validation | Purpose |
|---|---|
| Email Validation | Ensures correct email format |
| CNIC Validation | Enforces `XXXXX-XXXXXXX-X` format |
| Phone Validation | Checks valid phone number format |
| Date Validation | Prevents invalid date entries |
| Amount Validation | Blocks negative payment values |

Feedback is shown via color-coded messages:
- 🟢 **Green** — Success
- 🔴 **Red** — Error
- 🟡 **Yellow** — Warning

---

## Screenshots

> Dashboard showing live record counts across all modules.

> Judge module with Add / View All / Search / Update / Delete tabs.

> Case Management with client and judge ID linking.

> Case-Lawyer assignment table with role designation.

> Payment Management with quick status update.

*(Screenshots from the working Streamlit UI are in the `/screenshots` folder.)*

---

## Limitations

- No user authentication / login system
- No cloud storage or remote database support
- Limited file upload for evidence (paths stored, not files)
- No online appointment booking

---

## Future Improvements

- [ ] User authentication & role-based access
- [ ] Online appointment scheduling
- [ ] Cloud database integration (Azure SQL / Supabase)
- [ ] PDF report generation per case
- [ ] AI-based analytics (case outcome prediction)
- [ ] Email / SMS notification system

---

## Authors

| Name | Student ID |
|---|---|
| Hadia Laraib | 24F-5504 |
| Sameen Fatima | 24F-5524 |

**Course:** Database Systems Lab  
**Program:** BS FinTech  
**University:** FAST National University of Computer and Emerging Sciences  
**Semester:** Spring 2026  
**Instructor:** Naba Rahim

---

## References

1. [Python Official Documentation](https://docs.python.org)
2. [Streamlit Documentation](https://docs.streamlit.io)
3. [Microsoft SQL Server Documentation](https://learn.microsoft.com/en-us/sql/sql-server/)
4. [PyODBC Documentation](https://github.com/mkleehammer/pyodbc/wiki)

---

*This project was developed for educational purposes as part of the Database Systems Lab course.*
