from model_error import ErrorModel, EMPTY_LEX
import json

from model_language import LanguageModel

END_OF_WORD = "\n"
MAX_ERROR = 6  # adjust this parameter
ALPHA = 100000  # adjust this parameter
PREFIX_PATH = ""


# PREFIX_PATH = "../"


class BORtree:
    # print("prefix: " + PREFIX_PATH + "<-")
    ungram_distance = ErrorModel()
    ungram_distance.load_json(PREFIX_PATH + "fitted_levehshtein/statistics_1gram.json")
    bigram_distance = ErrorModel()
    bigram_distance.load_json(PREFIX_PATH + "fitted_levehshtein/statistics_2gram.json")
    frequency = LanguageModel()
    frequency.load_json(PREFIX_PATH + "fitted_language/statistics_1gram.json")

    def __init__(self):
        self.tree = [["", dict()]]
        self._tree_size = 0

    def fit(self, word):
        word += END_OF_WORD  # в дереве будет узел \n
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
        self.best_matches = {string: 0}
        self.error_threshold = len(string) * MAX_ERROR
        self._get_best_word(string)
        for key in self.best_matches:
            print("way: \"{}\" - frequency: {}*ALPHA : distance: {}".
                  format(key, (BORtree.frequency.get_popularity(key)),
                         BORtree.bigram_distance.get_weighted_distance(string, key)))

            self.best_matches[key] = (BORtree.frequency.get_popularity(key) * ALPHA) / \
                                     max(1, BORtree.bigram_distance.get_weighted_distance(string, key))
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
                if char == END_OF_WORD:
                    continue
                self._get_best_word(new_str,
                                    way + current_char,
                                    error + add_er + self._get_error(new_str[iteration], char),
                                    iteration,
                                    self.tree[node][1][char],
                                    big_err)
            return

        current_char = self.tree[node][0]

        if error > self.error_threshold:
            return
        if (END_OF_WORD in self.tree[node][1]) and (len(string) - 1 == iteration):
            self._add_match(way + current_char, error)
            # print("\"" + way + "\"" + " --:-- error: " + str(error))
            return
        if len(string) - 1 == iteration:
            return

        iteration += 1
        next_iteration(string)  # next letter

        if not big_err:  # пусть добавление или удаление буквы может быть только 1 раз
            big_err = True
            if len(string) - iteration > 1:  # dell letter
                add_error = self._get_error(string[iteration], EMPTY_LEX)
                next_iteration(string[:iteration] + string[iteration + 1:], add_error)

            for symbol in self.tree[node][1]:  # add letter
                add_error = self._get_error(EMPTY_LEX, symbol)
                next_iteration(string[:iteration] + symbol + string[iteration:], add_error)

    @staticmethod
    def _get_error(orig, fix):
        if orig == fix:
            # print("ERROR {}, orig \"{}\", fix \"{}\"".format(0, orig, fix))
            return 0

        # print("ERROR {}, orig \"{}\", fix \"{}\"".format(1 / BORtree.ungram_distance.get_gram_statistics(orig, fix),
        #                                                  orig, fix))
        # if (orig == "~") or (fix == "~"):
        #     return 50
        return 1 / BORtree.ungram_distance.get_gram_statistics(orig, fix)


if __name__ == "__main__":
    t = BORtree()

    t.load_json("fitted_tree/tree.json")
    # t.fit("кот")
    # t.fit("крот")
    # t.fit("коп")
    # t.fit("кошка")
    # t.fit("окошко")

    # for num, i in enumerate(t.tree):
    #     print("{} : {}".format(num, i))

    for i in t.find_best("трон"):
        print(i)

    # f = open("t1.txt", "w")
    # def print_words(_tree, node=0, word=""):
    #     word += _tree[node][0]
    #     if _tree[node][0] == '\n':
    #         f.write(word)
    #         return
    #     for key, value in _tree[node][1].items():
    #         print_words(_tree, value, word)
    # print_words(t.tree)
    # f.close()
