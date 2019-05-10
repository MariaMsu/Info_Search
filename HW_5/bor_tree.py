import pprint
from asyncio import sleep

from model_error import ErrorModel, EMPTY_LEX
import json

from model_language import LanguageModel
from time_decorator import timeit

END_OF_WORD = "\n"
MAX_ERROR = 4  # adjust this parameter
ALPHA = 1000000  # adjust this parameter
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
        self.tree = [["", dict(), None]]  # [current_letter, {letter: line ...}, word_of_this_node]
        self._tree_size = 0

    def fit(self, word):
        if not word:
            return

        i, node = self._find_node(word)
        if i == -1 and node == -1:
            return
        self._add_node(node, word[i])
        for char in word[i + 1:]:
            self._add_node(self._tree_size, char)
        self.tree[self._tree_size][2] = word

    def load_json(self, json_path):
        self.tree = json.loads(open(json_path, "r").read())

    def store_json(self, json_path):
        file = open(json_path, "w")
        file.write(json.dumps(self.tree))
        file.close()

    # вставляет словое, если оно является апефиксом или
    # находит позицию, с которой нужно вставлять новое слово
    def _find_node(self, word, iteration=0, node=0):
        if len(word) <= iteration:
            self.tree[node][2] = word
            return -1, -1
        char = word[iteration]
        if char in self.tree[node][1]:
            return self._find_node(word, iteration + 1, self.tree[node][1][char])
        return iteration, node

    def _add_node(self, node, char):
        self._tree_size += 1
        self.tree[node][1][char] = self._tree_size
        self.tree.append([char, dict(), None])

    def find_best(self, string):
        self.best_matches = {string: 0}
        self.error_threshold = len(string) * MAX_ERROR
        self.str = string
        self._get_best_word()
        for key in self.best_matches:
            # print("way: \"{}\" - frequency: {}*ALPHA : distance: {}".
            #       format(key, (BORtree.frequency.get_popularity(key)),
            #              BORtree.bigram_distance.get_weighted_distance(string, key)))

            self.best_matches[key] = (BORtree.frequency.get_popularity(key) * ALPHA) / \
                                     BORtree.bigram_distance.get_weighted_distance(string, key)
        return sorted(self.best_matches.items(), key=lambda kv: kv[1], reverse=True)

    # вставляем в словарь самых похожих слов
    def _add_match(self, way, score):
        if way not in self.best_matches:
            self.best_matches[way] = score
            return
        self.best_matches[way] = min(self.best_matches[way], score)

    # 2729.05 ms         new: 6308.29 ms
    def _get_best_word(self, error=0, pointer=-1, node=0, small_error=0, big_err=0):
        branches = self.tree[node][1]  # все возможные замены букв, идущие после этого префикса
        word = self.tree[node][2]  # слово этой вершины или none

        if error > self.error_threshold:
            return

        if word and (len(self.str) - 1 == pointer):
            self._add_match(word, error)
            # print("(local) \"" + word + "\"" + " --:-- error: " + str(error))
            return

        if len(self.str) - 1 <= pointer:
            return

        pointer += 1
        orig_char = self.str[pointer]
        for char, new_node in branches.items():
            self._get_best_word(
                error=error + self._get_error(orig_char, char),
                pointer=pointer,
                node=new_node,
                big_err=big_err)

            if big_err < 1:  # пусть добавление или удаление буквы может быть только 1 раз
                # вставка
                self._get_best_word(
                    error=error + self._get_error(EMPTY_LEX, char),
                    pointer=pointer - 1,
                    node=new_node,
                    big_err=big_err + 1)

        if big_err < 1:  # пусть добавление или удаление буквы может быть только 1 раз
            if len(self.str) - 1 > pointer:
                # print("len {}, pointer {}".format(len(self.str), pointer))
                orig_next_char = self.str[pointer + 1]
                next_node = branches.get(orig_next_char)
                if next_node:
                    # удаление
                    self._get_best_word(
                        error=error + self._get_error(orig_char, EMPTY_LEX),
                        pointer=pointer + 1,
                        node=next_node,
                        big_err=big_err + 1)
            # удаление последнего символа в слове
            elif word:
                error += self._get_error(orig_char, EMPTY_LEX)
                self._add_match(word, error)
                # print("(local) \"" + word + "\"" + " --:-- error: " + str(error))

    @staticmethod
    def _get_error(orig, fix):
        if orig == fix:
            # print("ERROR {}, orig \"{}\", fix \"{}\"".format(0, orig, fix))
            return 0

        # print("ERROR {}, orig \"{}\", fix \"{}\"".format(1 / BORtree.ungram_distance.get_gram_statistics(orig, fix),
        #                                                  orig, fix))
        # if (orig == "~") or (fix == "~"):
        #     return 50
        return 1 / BORtree.ungram_distance.get_popularity(orig, fix)


if __name__ == "__main__":
    t = BORtree()

    t.load_json("fitted_tree/tree.json")


    # t.fit("вк")
    # t.fit("в")
    # t.fit("коп")
    # t.fit("кошка")
    # t.fit("окошко")

    # pprint.pprint(t.tree)

    # for num, i in enumerate(t.tree):
    #     print("{} : {}".format(num, i))

    @timeit
    def a():
        for j in range(500):
            for i in t.find_best("кожка"):
                print(i)
        for j in range(500):
            for i in t.find_best("кирпич"):
                print(i)


    a()

    # for i in t.find_best("скота"):
    #     print(i)
