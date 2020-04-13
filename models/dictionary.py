from sqlalchemy import Integer, String, ForeignKey, ARRAY

from db import session


class Dictionary(session.Model):
    __tablename__ = 'dictionary'
    id = session.Column(Integer, primary_key=True, autoincrement=True)
    name = session.Column(String(50), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Dictionary(id={}, name={}".format(
            self.id, self.name
        )

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Word(session.Model):
    __tablename__ = 'word'
    id = session.Column(Integer, primary_key=True, autoincrement=True)
    word = session.Column(String(120), nullable=False)
    tone = session.Column(String(50), nullable=False, default='None')

    dictionaryId = session.Column(Integer, ForeignKey('dictionary.id'), nullable=False)
    dictionary = session.relationship('Dictionary', backref=session.backref('words', lazy=True))

    def __init__(self, dictionaryId, word, tone):
        self.dictionaryId = dictionaryId
        self.word = word
        self.tone = tone

    def __repr__(self):
        return "<Word(id={}, word={}, tone={}".format(
            self.id, self.word, self.tone
        )

    def __str__(self):
        return "{}_{}".format(self.word, self.part_of_speech)

    def serialize(self):
        return {
            'id': self.id,
            'word': self.word,
            'tone': self.tone,
            'dictionary_id': self.dictionaryId
        }
