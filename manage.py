import csv

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
        'words': {}
    }
    text = "Сегодня день не плохой, даже не ужасный, а очень хороший!"
    img = 'hand.png'

    return render_template("index.html", text=text, result=result, img=img)


@app.route('/analyze', methods=['POST'])
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


@app.route('/dictionaries/<name>', methods=['GET'])
def get_dictionaries(name):
    about_dictionary = ""
    dictionary = {}
    if name == 'chi_unigram':
        about_dictionary = "Словарь униграм, построенный с помощью критерия согласия Пирсона (Хи-квадрат)"
        with open('app/dictionaries/chi_plus.csv', encoding='utf-8') as f:
            dictionary = dict(filter(None, csv.reader(f)))
        dictionary.pop('term')
    elif name == 'cnn_unigram':
        about_dictionary = "Словарь униграм, построенный с помощью свёрточной нейронной сети"
    elif name == 'rusentilex':
        about_dictionary = "Словарь оценочных слов и выражений русского языка РуСентиЛекс (" \
                           "http://www.labinform.ru/pub/rusentilex/rusentilex_2016.txt) "
    elif name == 'chi_bigram':
        about_dictionary = "Словарь биграм, построенный с помощью критерия согласия Пирсона (Хи-квадрат)"
    return render_template("dictionaries.html", about_dictionary=about_dictionary, dictionary=dictionary)


@app.route('/about', methods=['GET'])
def about_project():
    return render_template("about.html")


@app.route('/analyze/files', methods=['GET'])
def files_classifier():
    return render_template("files_analyze.html")


if __name__ == '__main__':
    manager.run()
