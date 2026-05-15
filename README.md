# Multi-User Expense Tracker

A modern, user-centric Flask application for managing personal expenses with secure authentication and data isolation.

## 🚀 Tech Stack

- **Backend:** [Flask](https://flask.palletsprojects.com/)
- **Authentication:** [Flask-Login](https://flask-login.readthedocs.io/)
- **Security:** Werkzeug (Password Hashing)
- **Database:** SQLite & SQLAlchemy
- **Frontend:** Jinja2, Vanilla CSS/JS

## ✨ New Features: Authentication & Privacy

### 1. Secure User Accounts
- **Registration:** Users can create unique accounts with usernames and passwords.
- **Password Hashing:** Passwords are never stored in plain text; they are securely hashed using Werkzeug's `generate_password_hash`.
- **Validation:** Prevents duplicate registrations with the same username.

### 2. Data Isolation
- **Personal Dashboard:** Users only see their own expenses. Data from other users is completely inaccessible.
- **Ownership:** Every expense is linked to a specific user via a `user_id` foreign key.
- **Route Protection:** All CRUD operations are protected by `@login_required`. Accessing any page while unauthenticated redirects to the login screen.

### 3. Updated UI
- **User-Specific Navbar:** Shows a personalized welcome message and the user's username.
- **Auth Forms:** Clean, minimal Login and Registration pages.
- **Mobile Responsive:** All authentication features are fully optimized for mobile devices.

## 🛠️ Installation & Setup

1. **Install dependencies**:
   ```bash
   python3 -m pip install flask flask-sqlalchemy python-dotenv flask-login --break-system-packages
   ```
2. **Run the application**:
   ```bash
   python3 run.py
   ```
3. **Access the App**: Go to `http://127.0.0.1:5000` to register your account.

## 📁 Project Structure

```text
.
├── app/
│   ├── __init__.py      # App factory & Auth setup
│   ├── models.py        # User & Expense models (Relationship)
│   ├── routes.py        # Auth & Expense CRUD logic
│   ├── static/css/
│   │   └── style.css    # Responsive styles
│   └── templates/
│       ├── base.html    # Navbar with Auth state
│       ├── index.html   # User-specific dashboard
│       ├── login.html   # Login form
│       └── register.html# Registration form
└── run.py               # Entry point
```
