import math

from model_error import ErrorModel, EMPTY_LEX
import json

from model_language import LanguageModel

END_OF_WORD = "\n"
MAX_ERROR = 100
ALPHA = -1
ADD_LEX = "йцукенгшщзхъфывапролджэячсмитьбюё"

ungram_distance = ErrorModel()
ungram_distance.load_json("../fitted_levehshtein/statistics_1gram.json")

frequency = LanguageModel()
frequency.load_json("../fitted_language/statistics_1gram.json")


class BORtree:
    def __init__(self):
        self.tree = [["", dict()]]
        self._tree_size = 0

    def fit(self, word):
        word += END_OF_WORD
        i, node = self._find_node(word)

        self._add_node(node, word[i])
        for char in word[i + 1:]:
            self._add_node(self._tree_size, char)

    def load_json(self, json_path):
        self.tree = json.loads(open(json_path, "r").read())

    def store_json(self, json_path):
        file = open(json_path, "w")
        file.write(json.dumps(self.tree))
        file.close()

    def _find_node(self, word, iteration=0, node=0):
        char = word[iteration]
        if char in self.tree[node][1]:
            return self._find_node(word, iteration + 1, self.tree[node][1][char])
        return iteration, node

    def _add_node(self, node, char):
        self._tree_size += 1
        self.tree[node][1][char] = self._tree_size
        self.tree.append([char, dict()])

    def find_best(self, string):
        self.best_matches = {}
        self.error_threshold = len(string) * MAX_ERROR
        self._get_best_word(string + END_OF_WORD)
        for key in self.best_matches:
            print("{} : {}".format((frequency.get_popularity(key)**ALPHA), self.best_matches[key]))
            self.best_matches[key] = (frequency.get_popularity(key)**ALPHA) / self.best_matches[key]
        return sorted(self.best_matches.items(), key=lambda kv: kv[1], reverse=True)

    # вставляем в словарь самых похожих слов
    def _add_match(self, way, score):
        if way not in self.best_matches:
            self.best_matches[way] = score
        elif self.best_matches[way] > score:
            self.best_matches[way] = score

    def _get_best_word(self, string, way="", error=0, iteration=-1, node=0, big_err=False):
        def next_iteration(new_str, add_er=0):
            for char in self.tree[node][1]:
                self._get_best_word(new_str,
                                    way + current_char,
                                    error + add_er + self._get_error(new_str[iteration], char),
                                    iteration + 1,
                                    self.tree[node][1][char],
                                    big_err)

        if error > self.error_threshold:
            return
        if len(string) <= iteration:
            return
        if self.tree[node][0] == string[iteration] == END_OF_WORD:
            self._add_match(way, error)
            print(way + " - : - " + str(error))
            return

        current_char = self.tree[node][0]

        next_iteration(string)  # next letter

        if not big_err:  # добавление или удаление буквы может быть только 1 раз
            big_err = True
            if len(string) - iteration > 1:
                add_error = self._get_error(string[iteration], EMPTY_LEX)
                next_iteration(string[:iteration] + string[iteration + 1:], add_error)  # dell letter

            for symbol in ADD_LEX:
                add_error = self._get_error(EMPTY_LEX, symbol)
                next_iteration(string[:iteration] + symbol + string[iteration:], add_error)  # add letter

    @staticmethod
    def _get_error(orig, fix):
        return ungram_distance.get_weighted_distance(orig, fix)


if __name__ == "__main__":
    t = BORtree()

    t.fit("кот")
    t.fit("крот")
    t.fit("ком")
    t.fit("кошка")
    t.fit("кп")

    # for num, i in enumerate(t.tree):
    #     print("{} : {}".format(num, i))

    for i in t.find_best("коп").items():
        print(i)
