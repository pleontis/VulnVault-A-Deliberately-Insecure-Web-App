from flask import Flask

app = Flask(__name__)
app.secret_key = 'changeme123'

from app import routes
