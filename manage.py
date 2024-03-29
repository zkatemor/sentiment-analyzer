"""исходный код программы классификации текста по тональности"""
import csv
import os
import shutil

import pandas as pd
from werkzeug.utils import secure_filename

from dotenv import load_dotenv
from flask import render_template, request
from flask_restful import Api
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.api.views import DictionaryView, WordView
from app.services.random import Random
from app.services.reporter import Reporter
from db import session
from app.services.sentimental import Sentimental

load_dotenv()

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

app = create_app()

migrate = Migrate(app, session)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

api = Api(app)
api.add_resource(DictionaryView, '/dictionary')
api.add_resource(WordView, '/word')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FILENAME'] = ''
app.config['DICTIONARY'] = ['app/dictionaries/rusentilex.csv']
app.config['IS_UNIGRAM'] = True


# удаление старых файлов отчетов для экономии места на сервере
def delete_old_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


@app.route('/sentiment', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'GET':
            """home page"""
            result = {
                'score': 0,
                'positive': 0,
                'negative': 0,
                'comparative': 0,
                'words': {}
            }
            random = Random('app/static/reviews.json')
            text = random.get_review()
            img = 'icons/hand.png'
            positive = ''
            negative = ''
            modifier = ''
            report = ''
        else:
            delete_old_files('app/static/reports')
            text = request.form['text']
            select = request.form.get('select')
            dictionary = ['app/dictionaries/rusentilex.csv']
            is_unigram = True

            if str(select) == 'CHI unigram':
                dictionary = ['app/dictionaries/chi_minus.csv', 'app/dictionaries/chi_plus.csv']
                is_unigram = True
            elif str(select) == 'CNN unigram':
                dictionary = ['app/dictionaries/cnn_dict.csv']
                is_unigram = True
            elif str(select) == 'CHI bigram':
                dictionary = ['app/dictionaries/chi_collocations_minus.csv',
                              'app/dictionaries/chi_collocations_plus.csv']
                is_unigram = False

            sent = Sentimental(dictionary=dictionary,
                               negation='app/dictionaries/negations.csv',
                               modifier='app/dictionaries/modifier.csv',
                               is_unigram=is_unigram)
            result = sent.analyze(text)
            if result['score'] > 0:
                img = 'icons/positive.png'
            elif result['score'] == 0:
                img = 'icons/hand.png'
            else:
                img = 'icons/negative.png'

            positive_str = [str(s) for s in result['words']['positive']]
            positive = ", ".join(positive_str)

            negative_str = [str(s) for s in result['words']['negative']]
            negative = ", ".join(negative_str)

            mod_str = [str(s) for s in result['words']['modifier']]
            modifier = ", ".join(mod_str)

            report = Reporter(text, result).get_report()

        return render_template("index.html",
                               text=text,
                               result=result,
                               img=img,
                               positive=positive,
                               negative=negative,
                               modifier=modifier,
                               download_file=report)

    except Exception as e:
        print(e)


@app.route('/dictionaries/<name>', methods=['GET'])
def get_dictionaries(name):
    about_dictionary = ""
    name_dictionary = ""
    dictionary = {}
    html_file = ""
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
        with open('app/dictionaries/cnn_dict.csv', encoding='utf-8') as f:
            dictionary = dict(filter(None, csv.reader(f)))
        dictionary.pop('term')
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
    elif name == 'all':
        name_dictionary = "Словари оценочной лексики для классификации текстов по тональности"
        html_file = "all_dictionary.html"
        dictionary = dict(
            хороший=1,
            неплохой=0.5,
            нехороший=-0.5,
            плохой=-1
        )
    return render_template("dictionaries.html",
                           about_dictionary=about_dictionary,
                           dictionary=dictionary,
                           name_dictionary=name_dictionary,
                           html_file=html_file)


@app.route('/about', methods=['GET'])
def about_project():
    return render_template("about.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/analyze/files', methods=['GET', 'POST'])
def files_classifier():
    delete_old_files('app/static/reports')
    delete_old_files('app/static/uploads')
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            app.config['UPLOAD_FILENAME'] = filename
            select = request.form.get('select')
            if str(select) == 'CHI unigram':
                dictionary = ['app/dictionaries/chi_minus.csv', 'app/dictionaries/chi_plus.csv']
                is_unigram = True
            elif str(select) == 'CNN unigram':
                dictionary = ['app/dictionaries/cnn_dict.csv']
                is_unigram = True
            elif str(select) == 'RuSentiLex':
                dictionary = ['app/dictionaries/rusentilex.csv']
                is_unigram = True
            elif str(select) == 'CHI bigram':
                dictionary = ['app/dictionaries/chi_collocations_minus.csv',
                              'app/dictionaries/chi_collocations_plus.csv']
                is_unigram = False
            app.config['DICTIONARY'] = dictionary
            app.config['IS_UNIGRAM'] = is_unigram

    return render_template("files_analyze.html")


@app.route('/analyze/files/result', methods=['GET', 'POST'])
def ajax_files():
    if os.listdir(app.config['UPLOAD_FOLDER']):
        filename = 'app/static/uploads/' + app.config['UPLOAD_FILENAME']
        df = pd.read_excel(filename, sheet_name="Лист1")
        texts = df['text'].tolist()

        dictionary = app.config['DICTIONARY']
        is_unigram = app.config['IS_UNIGRAM']

        sent = Sentimental(dictionary=dictionary,
                           negation='app/dictionaries/negations.csv',
                           modifier='app/dictionaries/modifier.csv', is_unigram=is_unigram)
        report = []

        for text in texts:
            result = sent.analyze(text)
            report.append(Reporter(text, result).get_dict())

        download_file = Reporter.get_reports(report)
        return render_template('include_files.html', download_file=download_file)
    else:
        return '<h3>Файл ещё не загружен</h3>'


if __name__ == '__main__':
    manager.run()
