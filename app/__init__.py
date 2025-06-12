from flask import Flask
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'dev'
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_db():
    db_path = 'vulnvault.db'
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT);")
        conn.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'adminpass');")

# ✅ Run this after the app is fully initialized
with app.app_context():
    init_db()

from app import routes
