from dotenv import load_dotenv
from flask import render_template
from flask_restful import Api
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.api.views import DictionaryView, WordView
from db import session

load_dotenv()

app = create_app()

migrate = Migrate(app, session)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

api = Api(app)
api.add_resource(DictionaryView, '/dictionary')
api.add_resource(WordView, '/word')


@app.route('/sentiment', methods=['GET'])
def index():
    """home page"""
    return render_template("index.html")


if __name__ == '__main__':
    manager.run()
