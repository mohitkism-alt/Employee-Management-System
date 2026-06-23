
# Employee Management System (Streamlit + SQLite)

## Overview
A professional Employee Management System built with Python, Streamlit, and SQLite.

## Features
- Login authentication
- Employee CRUD (Add / Update / Delete)
- Dashboard metrics
- Average salary analytics
- Gender distribution summary
- SQLite database integration
- Responsive Streamlit UI

## Project Structure
```
employee management system/
│── app.py              # Main application
│── auth.py             # Login system
│── dashboard.py        # Dashboard widgets
│── database.py         # Database operations
│── employee_v2.db      # SQLite database
│── requirements.txt
│── README.md
└── exports/
    └── .streamlit/
        └── config.toml
```

## Installation

### 1. Create virtual environment
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run application
```bash
streamlit run app.py
```

## Default Login
Username: admin  
Password: 123

## Data Analysis Opportunities
- Salary insights
- Gender ratio
- Role-based employee analysis
- Growth tracking

## Future Improvements
- Export CSV / Excel
- Charts and analytics
- Role-based authentication
- Search and filtering
- Cloud deployment

## Tech Stack
Python • Streamlit • SQLite • Pandas

## Author
*Mohit Kumar*
