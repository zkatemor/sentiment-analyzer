import re
import os
import csv
from collections import defaultdict


class Sentimental(object):
    def __init__(self, dictionary=None, negation=None, modifier=None):
        if dictionary is None and negation is None and modifier is None:
            base_dir = os.path.dirname(__file__)
            dictionary = [os.path.join(base_dir, p) for p in ['dictionaries/rusentilex.csv']]
            negation = os.path.join(base_dir, 'dictionaries/negations.csv')
            modifier = os.path.join(base_dir, 'dictionaries/modifier.csv')

        self.dictionary = {}
        self.negations = set()
        self.modifiers = {}

        for wl_filename in self.__to_arg_list(dictionary):
            self.load_dictionary(wl_filename)
        for negations_filename in self.__to_arg_list(negation):
            self.load_negations(negations_filename)
        for modifier_filename in self.__to_arg_list(modifier):
            self.load_modifiers(modifier_filename)

        self.__negation_skip = {'очень', 'самый'}

    @staticmethod
    def __to_arg_list(obj):
        if obj is not None:
            if not isinstance(obj, list):
                obj = [obj]
        else:
            obj = []
        return obj

    def __is_prefixed_by_negation(self, token_idx, tokens):
        #   True if i != 0 and tokens[i - 1] in self.negations else False
        prev_idx = token_idx - 1
        if tokens[prev_idx] in self.__negation_skip:
            prev_idx -= 1

        is_prefixed = False
        if token_idx > 0 and prev_idx >= 0 and tokens[prev_idx] in self.negations:
            is_prefixed = True

        return is_prefixed, tokens[prev_idx]

    def __is_prefixed_by_modifier(self, token_idx, tokens):
        prev_idx = token_idx - 1
        percent = 0

        is_prefixed = False
        if token_idx > 0 and prev_idx >= 0 and tokens[prev_idx] in self.modifiers:
            is_prefixed = True
            percent = self.modifiers[tokens[prev_idx]]

        return is_prefixed, tokens[prev_idx], percent

    def load_negations(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            negations = set([row['token'] for row in reader])
        self.negations |= negations

    def load_modifiers(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            modifiers = {row['token']: row['percent'] for row in reader}
        self.modifiers.update(modifiers)

    def load_dictionary(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            dictionary = {row['term']: row['tone'] for row in reader}
        self.dictionary.update(dictionary)

    def analyze(self, sentence):
        sentence_clean = re.sub(r'[^\w ]', ' ', sentence.lower())
        tokens = sentence_clean.split()

        scores = defaultdict(float)
        words = defaultdict(set)
        comparative = 0

        for i, token in enumerate(tokens):
            is_prefixed_by_negation, negation = self.__is_prefixed_by_negation(i, tokens)
            is_prefixed_by_modifier, modifier, mod_percent = self.__is_prefixed_by_modifier(i, tokens)
            if token in self.dictionary:
                tone = self.dictionary[token]
                words[tone].add(token)
                score = 1 if tone == 'positive' else -1

                if not is_prefixed_by_negation:
                    scores[tone] += score
                else:
                    words['modifier'].add(negation)

                if is_prefixed_by_modifier:
                    scores[tone] += score * float(mod_percent)
                    words['modifier'].add(modifier)

        if len(tokens) > 0:
            comparative = (scores['positive'] + scores['negative']) / len(tokens)

        result = {
            'score': scores['positive'] + scores['negative'],
            'positive': scores['positive'],
            'negative': scores['negative'],
            'comparative': comparative,
            'words': words
        }

        return result
