from flask_restful import Resource, reqparse
from models.dictionary import Dictionary, Word
from db import session


class DictionaryView(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=False)
        args = parser.parse_args()

        if args['id']:
            if Dictionary.query.filter(Dictionary.id == args['id']).count():
                dictionaries = Dictionary.query.filter(Dictionary.id == args['id'])
                js = Dictionary.serialize(dictionaries[0])
            else:
                return {'message': 'Dictionary not found', 'result': {}}, 404
        else:
            dictionaries = Dictionary.query.all()
            js = [Dictionary.serialize(d) for d in dictionaries]

        return {'message': 'Success', 'result': js}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        dictionary = Dictionary(args['name'])

        session.session.add(dictionary)
        session.session.commit()
        return {'message': 'Success', 'result': {}}, 201, {'Location': '/dictionary/:' + str(dictionary.id)}


class WordView(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=False)
        args = parser.parse_args()

        if args['id']:
            if Word.query.filter(Word.id == args['id']).count():
                words = Word.query.filter(Word.id == args['id'])
                js = Word.serialize(words[0])
            else:
                return {'message': 'Word not found', 'result': {}}, 404
        else:
            words = Word.query.all()
            js = [Word.serialize(d) for d in words]

        return {'message': 'Success', 'result': js}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('word', required=True)
        parser.add_argument('part_of_speech', required=True)
        parser.add_argument('tone', required=True)
        parser.add_argument('dictionary_id', required=True)
        args = parser.parse_args()

        word = Word(args['dictionary_id'],
                    args['word'],
                    args['tone'],
                    args['part_of_speech']
                    )

        session.session.add(word)
        session.session.commit()
        return {'message': 'Success', 'result': {}}, 201, {'Location': '/word/:' + str(word.id)}
