from subprocess import call
from contextlib import closing
import random
import json
import shelve


class Dictator:
    list = []
    dictionary = {}
    user_config = {'score': 0, 'level': 0}
    word_base_len = 6
    current_word = ''

    index = 0
    score = 0
    stage_width = 0

    def __init__(self, number_of_words=10, stage_width=80):
        self. number_of_words = number_of_words
        self. stage_width = stage_width
        self.dictionary = json.load(open('./assets/dictionary-lc.json', 'r'))
        with closing(shelve.open('./data/user_shelf.db')) as s:
            if (s.get('default_user')):
                self.user_config = s.get('default_user')

        word_list = open('./assets/wordlist.txt', 'r')
        for word in word_list:
            if self.word_for_level(word):
                self.list.append(str.strip(word))
        word_list.close()

        random.shuffle(self.list)
        self.list = iter(self.list[0:self.number_of_words])

    def next_word(self):
        try:
            self.current_word = next(self.list)
        except StopIteration:
            self.current_word = None
            return False
        return True

    def play(self):
        if (self.current_word):
            call(['say', self.current_word])
            return True

    def play_definition(self):
        if (self.current_word):
            call(['say', self.dictionary[self.current_word]])
        return True

    def check_word(self, input_word):
        if (not self.current_word):
            return None
        current_meaning = self.dictionary[self.current_word]
        is_correct = (str.lower(input_word) == str.lower(self.current_word))
        if is_correct:
            updated_score = self.user_config.get('score') + 1
            updated_level = None
            if (updated_score != self.user_config.get('score') and
                    updated_score % 10 == 0):
                updated_level = self.user_config.get('level') + 1
            self.update_user_config(score=updated_score, level=updated_level)
        return [is_correct, self.current_word, input_word, current_meaning]

    def update_user_config(self, score=None, level=None, words_seen=None):
        with closing(shelve.open('./data/user_shelf.db')) as s:
            if score:
                self.user_config['score'] = score
            if level:
                self.user_config['level'] = level
            if words_seen:
                self.user_config['words_seen'] = words_seen
            s['default_user'] = self.user_config

    def get_user(self):
        return self.user_config

    def word_for_level(self, word):
        user_level = self.user_config.get('level')
        return len(word) < (self.word_base_len + user_level) and \
            len(word) > self.user_config.get('level')
