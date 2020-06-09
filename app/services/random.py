import json
import random


class Random:
    def __init__(self, filename):
        self.reviews = None
        self.load_review(filename)

    def load_review(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reviews = json.load(f)
        self.reviews = reviews

    def get_review(self):
        texts = [str(review['pluses']) + '\n' + str(review['minuses']) + '\n' + str(review['comment'])
                 for model in self.reviews for review in model]
        texts = list(map(lambda x: x.replace('None', ''), texts))
        return random.choice(texts)
