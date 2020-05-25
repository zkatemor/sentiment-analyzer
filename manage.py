from dotenv import load_dotenv
from flask import render_template, request, redirect
from flask_restful import Api
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.api.views import DictionaryView, WordView
from db import session
from app.services.sentimental import Sentimental

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
    result = {
        'score': 0,
        'positive': 0,
        'negative': 0,
        'comparative': 0,
        'words': {"positive": "ldld"}
    }
    text = "Сегодня день не плохой, даже не ужасный, а очень хороший!"
    img = 'hand.png'

    return render_template("index.html", text=text, result=result, img=img)


@app.route('/sentiment/analyzer', methods=['POST'])
def classifier():
    text = request.form['text']

    sent = Sentimental(dictionary=['app/dictionaries/rusentilex.csv'],
                       negation='app/dictionaries/negations.csv')
    result = sent.analyze(text)
    if result['score'] > 0:
        img = 'positive.png'
    elif result['score'] == 0:
        img = 'hand.png'
    else:
        img = 'negative.png'
    return render_template("index.html", text=text, result=result, img=img)


if __name__ == '__main__':
    manager.run()
