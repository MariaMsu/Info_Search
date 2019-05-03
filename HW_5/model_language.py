import json


class LanguageModel:
    def __init__(self):
        self.dictionary = {}  # {item: prop}
        self._statistics_size = 0

    def fit(self, word_list):
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
        return ["^", "_"]
    word_list = ["^"] + string.split(" ") + ["_"]
    new_list = []
    for i in range(len(word_list) - 1):
        new_list += [(word_list[i], word_list[i + 1])]
    return new_list
