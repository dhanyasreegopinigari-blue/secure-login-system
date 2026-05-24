from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import text
from datetime import timedelta
from urllib.parse import quote_plus
import pyotp
import re
import threading
import webbrowser

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to continue.'
login_manager.login_message_category = 'info'

# Database Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    otp_secret = db.Column(db.String(16), nullable=True)
    two_factor_enabled = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validation
        if not username or len(username.strip()) < 3:
            flash('Username must be at least 3 characters', 'danger')
            return redirect(url_for('register'))

        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email format', 'danger')
            return redirect(url_for('register'))

        if not password or len(password) < 8:
            flash('Password must be at least 8 characters', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()

        if existing_user:
            if existing_user.email == email:
                flash('Email already exists', 'warning')
            else:
                flash('Username already exists', 'warning')
            return redirect(url_for('register'))

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Save user
        new_user = User(
            username=username.strip(),
            email=email.strip().lower(),
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email.strip().lower()).first()

        if user and bcrypt.check_password_hash(user.password, password):
            if user.two_factor_enabled and user.otp_secret:
                session['pre_2fa_userid'] = user.id
                flash('Enter the 2FA code from your authenticator app.', 'info')
                return redirect(url_for('two_factor'))

            session.permanent = True
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid email or password', 'danger')

    return render_template('login.html')

# Two-Factor Authentication Route
@app.route('/two-factor', methods=['GET', 'POST'])
def two_factor():
    pending_user_id = session.get('pre_2fa_userid')
    if not pending_user_id:
        return redirect(url_for('login'))

    user = User.query.get(pending_user_id)
    if not user or not user.two_factor_enabled or not user.otp_secret:
        session.pop('pre_2fa_userid', None)
        return redirect(url_for('login'))

    if request.method == 'POST':
        token = request.form.get('token', '').strip()
        if pyotp.TOTP(user.otp_secret).verify(token, valid_window=1):
            session.pop('pre_2fa_userid', None)
            session.permanent = True
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid authentication code', 'danger')

    return render_template('two_factor.html')

# Setup 2FA Route
@app.route('/setup-2fa', methods=['GET', 'POST'])
@login_required
def setup_2fa():
    user = current_user

    if user.two_factor_enabled and user.otp_secret:
        return render_template('setup_2fa.html', enabled=True)

    secret = session.get('otp_setup_secret') or user.otp_secret or pyotp.random_base32()
    session['otp_setup_secret'] = secret
    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=current_user.email, issuer_name='Secure Login System')
    qr_code_url = 'https://chart.googleapis.com/chart?chs=250x250&chld=M|0&cht=qr&chl=' + quote_plus(otp_uri)

    if request.method == 'POST':
        token = request.form.get('token', '').strip()
        if pyotp.TOTP(secret).verify(token, valid_window=1):
            user.otp_secret = secret
            user.two_factor_enabled = True
            db.session.commit()
            session.pop('otp_setup_secret', None)
            flash('Two-factor authentication enabled.', 'success')
            return redirect(url_for('dashboard'))

        flash('Unable to verify code. Please try again.', 'danger')

    return render_template('setup_2fa.html', enabled=False, otp_secret=secret, qr_code_url=qr_code_url)

# Disable 2FA Route
@app.route('/disable-2fa')
@login_required
def disable_2fa():
    user = current_user
    user.two_factor_enabled = False
    user.otp_secret = None
    db.session.commit()
    flash('Two-factor authentication has been disabled.', 'info')
    return redirect(url_for('dashboard'))

# Dashboard Route
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))

# Create Database
with app.app_context():
    db.create_all()
    if db.engine.dialect.name == 'sqlite':
        conn = db.engine.connect()
        current_columns = [row[1] for row in conn.execute(text("PRAGMA table_info('user')"))]
        if 'otp_secret' not in current_columns:
            conn.exec_driver_sql("ALTER TABLE user ADD COLUMN otp_secret VARCHAR(16)")
        if 'two_factor_enabled' not in current_columns:
            conn.exec_driver_sql("ALTER TABLE user ADD COLUMN two_factor_enabled BOOLEAN DEFAULT 0")
        conn.close()

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True, use_reloader=False)