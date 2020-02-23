from flask import render_template

from . import app


@app.route('/', methods=['GET'])
def index():
    """home page"""
    return render_template("index.html")