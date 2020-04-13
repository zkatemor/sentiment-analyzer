import os

from dotenv import load_dotenv
from flask import render_template, Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
session = SQLAlchemy(app)

from models.dictionary import Dictionary, Word


@app.route('/sentiment', methods=['GET'])
def index():
    """home page"""
    return render_template("index.html")
