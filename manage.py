import csv
import os

from werkzeug.utils import secure_filename

from dotenv import load_dotenv
from flask import render_template, request, redirect, make_response, url_for
from flask_restful import Api
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.api.views import DictionaryView, WordView
from db import session
from app.services.sentimental import Sentimental

load_dotenv()

UPLOAD_FOLDER = 'app/texts/uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'json'}

app = create_app()

migrate = Migrate(app, session)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

api = Api(app)
api.add_resource(DictionaryView, '/dictionary')
api.add_resource(WordView, '/word')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    positive = ""
    negative = ""
    modifier = ""
    return render_template("index.html", text=text, result=result, img=img, positive=positive, negative=negative,
                           modifier=modifier)


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

    positive_str = [str(s) for s in result['words']['positive']]
    positive = ", ".join(positive_str)

    negative_str = [str(s) for s in result['words']['negative']]
    negative = ", ".join(negative_str)

    mod_str = [str(s) for s in result['words']['modifier']]
    modifier = ", ".join(mod_str)

    return render_template("index.html", text=text, result=result, img=img, positive=positive, negative=negative,
                           modifier=modifier)


@app.route('/dictionaries/<name>', methods=['GET'])
def get_dictionaries(name):
    about_dictionary = ""
    name_dictionary = ""
    dictionary = {}
    if name == 'chi_unigram':
        name_dictionary = "Словарь униграм, построенный с помощью критерия согласия Пирсона (Хи-квадрат)"
        about_dictionary = "Распределение тонально-окрашенных слов с помощью критерия анализа – оценки корреляции " \
                           "двух событий: «слово содержится в корпусе» и «слово содержится в подкорпусе " \
                           "достоинств или недостатков». Благодаря методу, основанному на распределении оценочных слов " \
                           "с помощью критерия согласия Пирсона, удалось получить 1260 положительно окрашенных слов и " \
                           "2267 с отрицательной окраской."
        with open('app/dictionaries/chi_plus.csv', encoding='utf-8') as f:
            dictionary = dict(filter(None, csv.reader(f)))
        dictionary.pop('term')
        with open('app/dictionaries/chi_minus.csv', encoding='utf-8') as f:
            dictionary_minus = dict(filter(None, csv.reader(f)))
        dictionary_minus.pop('term')
        dictionary.update(dictionary_minus)
    elif name == 'cnn_unigram':
        name_dictionary = "Словарь униграм, построенный с помощью свёрточной нейронной сети"
        about_dictionary = "Обученная с помощью сверточной нейросети модель и предобученной модели векторных " \
                           "представлений слов Word2Vec показала следующие результаты: удалось выявить 373 " \
                           "положительно-окрашенных слов, 5216 отрицательно-окрашенных слов и 114 " \
                           "нейтрально-окрашенных слов. Данное распределение связано с тем, что и размеченные данных, " \
                           "взятые из словаря RuSentiLex не были сбалансированными (отрицательных слов 7148, " \
                           "положительных – 2774 и нейтральных – 746)."
    elif name == 'chi_bigram':
        name_dictionary = "Словарь биграм, построенный с помощью критерия согласия Пирсона (Хи-квадрат)"
        about_dictionary = "Распределение тонально-окрашенных словосочетаний с помощью критерия анализа – оценки " \
                           "корреляции " \
                           "двух событий: «слововочетание содержится в корпусе» и «словосочетание содержится в " \
                           "подкорпусе " \
                           "достоинств или недостатков». Благодаря методу, основанному на распределении оценочных слов " \
                           "с помощью критерия согласия Пирсона, удалось получить 20520 положительно окрашенных " \
                           "словосочетаний и " \
                           "19550 с отрицательной окраской."
        with open('app/dictionaries/chi_collocations_plus.csv', encoding='utf-8') as f:
            dictionary = dict(filter(None, csv.reader(f)))
        dictionary.pop('term')
        with open('app/dictionaries/chi_collocations_minus.csv', encoding='utf-8') as f:
            dictionary_minus = dict(filter(None, csv.reader(f)))
        dictionary_minus.pop('term')
        dictionary.update(dictionary_minus)
    return render_template("dictionaries.html", about_dictionary=about_dictionary, dictionary=dictionary,
                           name_dictionary=name_dictionary)


@app.route('/about', methods=['GET'])
def about_project():
    return render_template("about.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/analyze/files', methods=['GET', 'POST'])
def files_classifier():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("files_analyze.html")


if __name__ == '__main__':
    manager.run()
