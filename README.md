# Flask Authentication Project

This is a simple Flask-based web application that supports manual login and Google OAuth authentication. It also includes Selenium-based test cases for automated testing of the login functionality.

---

## Features

1. **Manual Login:** Supports login with email or phone number.
2. **Google OAuth:** Login using Google authentication.
3. **Session Management:** Utilizes Flask session for user management.
4. **Automated Tests:** Selenium-based tests for login and logout flows.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/memduhtutus/458.git
cd 458

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


pip install -r requirements.txt


python app.py


python testcase.py
```

### To run testcase.py

You may need to edit the webdriver. It is Chrome by default.
