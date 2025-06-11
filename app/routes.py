from flask import render_template, request, redirect, session, make_response
from app import app
import sqlite3
import os

app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

comments = []
db_path = 'vulnvault.db'

def init_db():
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT);")
        conn.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'adminpass');")

@app.before_first_request
def setup():
    init_db()

@app.route('/')
def index():
    return render_template('index.html', comments=comments)

@app.route('/comment', methods=['POST'])
def comment():
    text = request.form['comment']
    comments.append(text)  # XSS vulnerability
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"  # SQL Injection
        with sqlite3.connect(db_path) as conn:
            result = conn.execute(query).fetchone()
            if result:
                session['user'] = username
                return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session['user'])

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        if request.form.get('email'):
            return f"Email updated to: {request.form['email']}"  # CSRF vulnerability (no token)
    return render_template('profile.html')

@app.route('/invoice/<int:invoice_id>')
def invoice(invoice_id):
    if invoice_id == 1:
        return "Invoice #1 for Alice"
    elif invoice_id == 2:
        return "Invoice #2 for Bob"
    else:
        return "Access Denied"  # IDOR vulnerability (no auth check)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)  # Insecure file upload
    return f"Uploaded {file.filename} to {file_path}"
