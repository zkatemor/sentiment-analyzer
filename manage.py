from dotenv import load_dotenv
from flask import render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from apps import create_app
from db import session

load_dotenv()

app = create_app()

migrate = Migrate(app, session)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@app.route('/sentiment', methods=['GET'])
def index():
    """home page"""
    return render_template("index.html")


if __name__ == '__main__':
    manager.run()
