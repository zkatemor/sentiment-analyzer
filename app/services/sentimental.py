import os
import csv
import pymorphy2
import nltk
from collections import defaultdict


class Sentimental(object):
    def __init__(self, dictionary=None, negation=None, modifier=None, is_unigram=True):
        self.morph = pymorphy2.MorphAnalyzer()

        if dictionary is None and negation is None and modifier is None:
            base_dir = os.path.dirname(__file__)
            dictionary = [os.path.join(base_dir, p) for p in ['dictionaries/rusentilex.csv']]
            negation = os.path.join(base_dir, 'dictionaries/negations.csv')
            modifier = os.path.join(base_dir, 'dictionaries/modifier.csv')

        self.dictionary = {}
        self.negations = set()
        self.modifiers = {}
        self.is_unigram = is_unigram

        for wl_filename in self.__to_arg_list(dictionary):
            self.load_dictionary(wl_filename)
        for negations_filename in self.__to_arg_list(negation):
            self.load_negations(negations_filename)
        for modifier_filename in self.__to_arg_list(modifier):
            self.load_modifiers(modifier_filename)

        self.__negation_skip = {'очень', 'самый', 'достаточно', 'должен'}

    @staticmethod
    def __to_arg_list(obj):
        if obj is not None:
            if not isinstance(obj, list):
                obj = [obj]
        else:
            obj = []
        return obj

    def __is_prefixed_by_negation(self, token_idx, tokens):
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
            if self.is_unigram:
                dictionary = {self.__delete_part_of_speech(row['term']): row['weight'] for row in reader}
            else:
                dictionary = {self.__delete_part_of_speech(row['term']): row['weight'] for row in reader}
        self.dictionary.update(dictionary)

    def __get_tokens(self, sentence):
        # удаляем все символы, кроме кириллицы
        regex_tokenizer = nltk.tokenize.RegexpTokenizer('[а-яА-ЯЁё]+')
        # приводим к нижнему регистру
        words = regex_tokenizer.tokenize(sentence.lower())
        # приводим каждое слово в нормальную форму и добавляем тег - часть речи
        result = [self.morph.parse(w)[0].normal_form for w in words]
        return result

    def __get_bigrams(self, sentence):
        regex_tokenizer = nltk.tokenize.RegexpTokenizer('[а-яА-ЯЁё]+')
        words = regex_tokenizer.tokenize(sentence.lower())
        result = [self.morph.parse(words[i])[0].normal_form + ' ' + self.morph.parse(words[i + 1])[0].normal_form
                  for i in range(0, len(words) - 1)]
        return result

    # удаление части речи в слова или словосочетании
    def __delete_part_of_speech(self, term):
        if self.is_unigram:
            new_term = term[:-5]
        else:
            terms = term.split()
            new_term = terms[0][:-5] + ' ' + terms[1][:-5]
        return new_term

    def analyze(self, sentence):
        if self.is_unigram:
            terms = self.__get_tokens(sentence)
        else:
            terms = self.__get_bigrams(sentence)

        scores = defaultdict(float)
        words = defaultdict(set)
        comparative = 0

        for i, term in enumerate(terms):
            is_prefixed_by_negation, negation = self.__is_prefixed_by_negation(i, terms)
            is_prefixed_by_modifier, modifier, mod_percent = self.__is_prefixed_by_modifier(i, terms)
            if term in self.dictionary:
                tone = 'positive' if float(self.dictionary[term]) > 0 else 'negative'
                score = float(self.dictionary[term])
                words[tone].add(term)

                if is_prefixed_by_negation:
                    scores[tone] += score * -1
                    words['modifier'].add(negation)
                else:
                    scores[tone] += score

                if is_prefixed_by_modifier:
                    scores[tone] += score * float(mod_percent)
                    words['modifier'].add(modifier)

        if len(terms) > 0:
            comparative = (scores['positive'] + scores['negative']) / len(terms)

        result = {
            'score': scores['positive'] + scores['negative'],
            'positive': scores['positive'],
            'negative': scores['negative'],
            'comparative': comparative,
            'words': words
        }

        return result
