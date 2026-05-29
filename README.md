# Secure Login System🛡️

A secure authentication web application built using Flask.
The project includes user registration, login, logout, session management, password hashing using bcrypt, and input validation to enhance security. It also protects against common vulnerabilities such as SQL Injection through the use of SQLAlchemy ORM.

# Live Demo↗️

https://secure-login-system-7kh1.onrender.com/login

# Secure Login System✨

A secure authentication web application developed using Flask that provides user registration, login, logout, password hashing, session management, and protection against common web vulnerabilities such as SQL Injection.

---
##Screenshots✨
[Dashboard]
<img width="1080" height="2277" alt="secure login sysytem image" src="https://github.com/user-attachments/assets/e40f6928-e51a-4332-9aa4-b14ca2ab2418" />


## Project Overview🎐

The Secure Login System is a cybersecurity-focused web application built using Flask and SQLite to provide secure user authentication and account management. The project implements password hashing using bcrypt, secure session handling, input validation, and protected routes to enhance application security. It demonstrates secure coding practices and real-world authentication workflows commonly used in modern web applications.

---

## Features❄️

- User Registration System
- Secure User Login
- Password Hashing using bcrypt
- Session Management
- Logout Functionality
- Input Validation
- SQL Injection Protection using SQLAlchemy
- Protected Dashboard Route
- Responsive User Interface
- Flash Messages for User Feedback

---

## Technologies Used🚀

- Python
- Flask
- SQLite
- SQLAlchemy
- Flask-Bcrypt
- Flask-Login
- HTML5
- CSS3

---

## Project Structure🍀

```bash
secure-login-system/
│
├── app.py
├── requirements.txt
├── database.db
│
├── templates/
│   ├── register.html
│   ├── login.html
│   └── dashboard.html
│
├── static/
│   └── style.css
│
└── README.md
```

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/dhanyasreegopinigari-blue/secure-login-system.git
```

### 2. Navigate to Project Folder

```bash
cd secure-login-system
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### 5. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

### 7. Open in Browser

```bash
http://127.0.0.1:5000
```

---

## Security Features

### Password Hashing
Passwords are securely hashed using bcrypt before storing in the database.

### SQL Injection Protection
SQLAlchemy ORM prevents SQL injection attacks by safely handling database queries.

### Session Management
Authenticated user sessions are managed securely using Flask-Login.

### Protected Routes
Restricted pages are accessible only after successful login.

---

## Expected Outcome

The project provides a secure login authentication system that protects user credentials and minimizes unauthorized access using modern authentication and security techniques.

---

## Future Improvements🚀

- Two-Factor Authentication (2FA)
- Email Verification
- Password Reset System
- Remember Me Functionality
- Account Lockout After Multiple Failed Attempts
- JWT Authentication
- Admin Dashboard

---

## Deployment🎐

This project can be deployed using:

- Render
- Railway
- PythonAnywhere
- Heroku

---

## Author

**Dhanyasree Gopinigari**

GitHub: https://github.com/dhanyasreegopinigari-blue/

LinkedIn: https://www.linkedin.com/in/dhanyasree-gopinigari-694378409/

---

## License

This project is developed for educational and learning purposes.
