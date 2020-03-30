from dotenv import load_dotenv
from app import create_app
from flask import render_template
load_dotenv()

app = create_app()


@app.route('/sentiment', methods=['GET'])
def index():
    """home page"""
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
