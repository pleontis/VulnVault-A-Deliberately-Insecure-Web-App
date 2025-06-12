from flask import render_template, request, redirect, session
from app import app
import os
import sqlite3

comments = []
db_path = 'vulnvault.db'

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
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"  # SQL Injection
        with sqlite3.connect(db_path) as conn:
            result = conn.execute(query).fetchone()
            if result:
                session['user'] = username
                return redirect('/dashboard')
            else:
                error = "Invalid credentials"
    return render_template('login.html', error=error)

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
    fake_invoices = {
        1: {"name": "Alice", "invoice_id": 1, "amount": "$150.00", "date": "2025-06-01", "items": [
            {"item": "Web hosting", "price": "$50.00"},
            {"item": "Domain name", "price": "$20.00"},
            {"item": "SSL Certificate", "price": "$80.00"},
        ]},
        2: {"name": "Bob", "invoice_id": 2, "amount": "$99.00", "date": "2025-06-03", "items": [
            {"item": "Email Services", "price": "$49.00"},
            {"item": "Maintenance", "price": "$50.00"},
        ]}
    }

    invoice = fake_invoices.get(invoice_id)
    if invoice:
        return render_template("invoice.html", invoice=invoice)
    else:
        return "Access Denied"
# @app.route('/invoice/<int:invoice_id>')
# def invoice(invoice_id):
#     if invoice_id == 1:
#         return "Invoice #1 for Alice"
#     elif invoice_id == 2:
#         return "Invoice #2 for Bob"
#     else:
#         return "Access Denied"  # IDOR vulnerability

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)  # Insecure file upload
    return f"Uploaded {file.filename} to {file_path}"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')