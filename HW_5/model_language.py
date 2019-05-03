import json
import re

# def split(string):
#     word_list =  re.split("[ !@#№$%^&*()_\-+=[\]{}|;:\"'/?<>,\\\«»0123456789]", string)  # add "\"?
#     return [i for i in word_list if i]  # remove empty

MAX_WORD_LEN = 15


def split(string):
    word_list = []
    word = str()
    for char in string:
        if ("A" <= char <= "Z") or ("a" <= char <= "z") or ("А" <= char <= "Я") or ("а" <= char <= "я"):
            word += char
        elif word:
            if len(word) < MAX_WORD_LEN:
                word_list += [word]
            word = str()
    if word:
        word_list += [word]
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

    def prichesat_statistiku(self):
        for item in self.dictionary.keys():
            self.dictionary[item] /= self._statistics_size

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


if __name__ == "__main__":
    s = split("купить фисташки мачо опт украина")
    for i in s:
        print(i)
