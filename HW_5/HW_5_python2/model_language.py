# -*- coding: utf-8 -*-

import json

MAX_WORD_LEN = 15


def split(string):
    string += " "
    word_list = []
    word = str()
    for char in string:
        if (u"A" <= char <= u"Z") or (u"a" <= char <= u"z") or (u"А" <= char <= u"Я") or (u"а" <= char <= u"я"):
            word += char
        elif word:
            if len(word) < MAX_WORD_LEN:
                word_list += [word]
            word = str()
    return word_list


class LanguageModel:
    def __init__(self):
        self.dictionary = {}  # {item: prop}
        self._statistics_size = 0

    def fit(self, word_list):
        if not word_list:
            return
        for item in word_list:
            self._add_statistics(item)

    def load_json(self, json_path):
        (size, stat) = json.loads(open(json_path, "r").read())
        self._statistics_size, self.dictionary = size, stat

    def store_json(self, json_path):
        file = open(json_path, "w")
        file.write(json.dumps((self._statistics_size, self.dictionary)))
        file.close()

    def _add_statistics(self, item):
        self.dictionary.setdefault(item, 0)
        self.dictionary[item] += 1
        self._statistics_size += 1

    def prichesat_statistiku(self, cut_off=0):
        for key in list(self.dictionary.keys()):  # to avoid "RuntimeError: dictionary changed size during iteration
            self.dictionary[key] = float(self.dictionary[key])
            frequency = self.dictionary[key] / self._statistics_size
            if frequency > cut_off:
                self.dictionary[key] = frequency
            else:
                self.dictionary.pop(key)

    # return (кол-во вхождений данного элемента / размер статистики)
    def get_popularity(self, item):
        if item in self.dictionary:
            return self.dictionary[item]
        return 0.5 / self._statistics_size  # newer sow this case


# represent word as bigrams
def bi_word(string):
    if not string:
        return []
    word_list = ["^"] + split(string) + ["_"]
    new_list = []
    for i in range(len(word_list) - 1):
        new_list += [str(word_list[i] + word_list[i + 1])]
    return new_list


# делает биграммы из листа слов
def create_pair_from_list(word_list):
    if not word_list:
        return []
    pair_list = ["^" + word_list[0]]
    for i in range(len(word_list) - 1):
        pair_list += [word_list[i] + word_list[i + 1]]
    pair_list += [word_list[-1] + "_"]
    return pair_list


if __name__ == "__main__":
    s = split("купить фисташки мачо опт украина")
    for i in s:
        print(i)
