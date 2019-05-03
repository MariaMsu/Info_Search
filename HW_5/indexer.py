# -*- coding: utf-8 -*-
import sys
import numpy as np

reload(sys)
sys.setdefaultencoding('utf8')


# represent word as bigrams
def make_bigram(string):
    if not string:
        return ["^_"]
    new_string = ["^" + string[0]]
    for i in range(len(string) - 1):
        new_string += [string[i:i + 2]]
    new_string += [string[-1:] + "_"]
    return new_string


class ErrorStatistics:
    def __init__(self):
        self.statistics = dict()  # {"origin" : {"fix" : number}}
        self._statistics_size = 0

    def ne_fit(self, a, b):
        levenshtein_matrix = self._get_levenshtein_matrix(a, b)
        self._fill_statistics(a, b, levenshtein_matrix)

    def prichesat_statistiku(self):
        for orig in self.statistics.keys():
            for fix in self.statistics[orig].keys():
                self.statistics[orig][fix] /= self._statistics_size

    def get_weighted_distance(self, a, b):
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n,m)) space
            a, b = b, a
            n, m = m, n

        current_row = list(range(n + 1))  # Keep current and previous row, not entire matrix
        # matrix = np.array([current_row])
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = (previous_row[j] + 1) / self._get_statistics("~", b[i - 1]), \
                                      (current_row[j - 1] + 1) / self._get_statistics(a[j - 1], "~"), \
                                      (previous_row[j - 1] + int(a[j - 1] != b[i - 1])) / self._get_statistics(a[j - 1],
                                                                                                               b[i - 1])
                current_row[j] = min(add, delete, change)
            # matrix = np.vstack((matrix, [current_row]))
        return current_row[n]

    def _get_statistics(self, orig, fit):
        if orig in self.statistics and fit in self.statistics[orig]:
            return self.statistics[orig][fit]
        return 0.5 / self._statistics_size  # newer sow this case

    def _add_statistics(self, orig, fix):
        self.statistics.setdefault(orig, dict())
        self.statistics[orig].setdefault(fix, 0)
        self.statistics[orig][fix] += 1
        self._statistics_size += 1

    def _fill_statistics(self, a, b, matrix):
        n, m = len(a), len(b)

        position = [n, m, matrix[m, n]]  # [x, y, distance]
        while position[2] != 0:  # пока position не придет в правый нижний угол
            x, y = position[0], position[1]

            possible_actions = [matrix[y - 1][x - 1],  # change
                                matrix[y - 1][x],  # add
                                matrix[y][x - 1]]  # delete
            action = np.argmin(possible_actions)

            if action == 0:  # change
                if position[2] != possible_actions[action.item()]:
                    position[2] -= 1
                    self._add_statistics(a[x - 1], b[y - 1])
                    # print(a[x - 1] + " -> " + b[y - 1])
                position[0] -= 1
                position[1] -= 1
            elif action == 1:  # add
                if position[2] != possible_actions[action.item()]:
                    position[2] -= 1
                    self._add_statistics("~", b[y - 1])
                    # print("~ -> " + b[y - 1])
                position[1] -= 1
            else:  # delete
                if position[2] != possible_actions[action.item()]:
                    position[2] -= 1
                    self._add_statistics(a[x - 1], "~")
                    # print(a[x - 1] + " -> ~")
                position[0] -= 1

    @staticmethod
    def _get_levenshtein_matrix(a, b):
        n, m = len(a), len(b)
        inverse = False
        if n > m:
            # Make sure n <= m, to use O(min(n,m)) space
            a, b = b, a
            n, m = m, n
            inverse = True

        current_row = list(range(n + 1))  # Keep current and previous row, not entire matrix
        matrix = np.array([current_row])
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, \
                                      current_row[j - 1] + 1, \
                                      previous_row[j - 1] + int(a[j - 1] != b[i - 1])
                current_row[j] = min(add, delete, change)
            matrix = np.vstack((matrix, [current_row]))
        return matrix if not inverse else matrix.T


class LanguageModel:
    def __init__(self):
        self.un_prop = {}  # {word : prop}
        self.un_count = 0.0
        self.bin_prop = {}  # {first_word : {second_word : prop}}
        self.bin_count = 0.0

        self.default_un_prop = 0
        self.default_bin_prop = 0

        self.all_words = set()

    def create_model(self, file_name):
        with open(file_name) as file:
            for line in file:
                tab_ind = line.find('\t')
                if tab_ind != -1:
                    line = line[tab_ind + 1:]
                line = line.lower()
                words = line.split(" ")

                self.all_words.update(set(words))

                len_words = len(words)
                for i in range(len_words):
                    self.un_count += 1
                    if words[i] in self.un_prop:
                        self.un_prop[words[i]] += 1
                    else:
                        self.un_prop[words[i]] = 1

                    if i < len_words - 1:
                        self.bin_count += 1

                        if words[i] in self.bin_prop:
                            if words[i + 1] in self.bin_prop[words[i]]:
                                self.bin_prop[words[i]][words[i + 1]] += 1
                            else:
                                self.bin_prop[words[i]][words[i + 1]] = 1
                        else:
                            self.bin_prop[words[i]] = {words[i + 1]: 1}
            for ind in self.un_prop:
                self.un_prop[ind] = self.un_prop[ind] / self.un_count
            for ind in self.bin_prop:
                for i_ind in self.bin_prop[ind]:
                    self.bin_prop[ind][i_ind] = self.bin_prop[ind][i_ind] / self.bin_count

            self.default_un_prop = 1 / self.un_count
            self.default_bin_prop = 1 / self.bin_count

    def get_un_prop(self, word):
        word = word.encode("utf8")
        if word in self.un_prop:
            return self.un_prop[word]
        else:
            return self.default_un_prop

    def get_bin_prop(self, first, second):
        if first in self.bin_prop:
            if second in self.bin_prop[first]:
                return self.bin_prop[first][second]
            else:
                return self.default_bin_prop
        else:
            return self.default_bin_prop

    # print probabilities for all words
    def print_all_un(self):
        for ind in self.un_prop:
            print("{}:\t{}".format(ind, self.un_prop[ind]))

    # print probabilities for all words pairs
    def print_all_bin(self):
        for ind in self.bin_prop:
            for i_ind in self.bin_prop[ind]:
                print("({}, {}):\t{}".format(ind, i_ind, self.bin_prop[ind][i_ind]))

    def get_P_for_query(self, query):
        query = query.lower()
        words = query.split(" ")
        len_words = len(words)
        probs = np.zeros(len_words + (len_words - 1))
        probs_ind = 0
        for i in range(len_words):
            probs[probs_ind] = self.get_un_prop(words[i])
            probs_ind += 1
            if i < len_words - 1:
                probs[probs_ind] = self.get_bin_prop(words[i], words[i + 1])
                probs_ind += 1
        return np.prod(probs)

    def get_most_relevant_after_word(self, word):
        if word not in self.bin_prop:
            return []
        l = list(self.bin_prop[word].items())
        l.sort(key=lambda x: x[1], reverse=True)
        return [item[0].decode() for item in l]

    def get_all_words(self):
        return self.all_words


class BORtree:
    def __init__(self):
        self.lit = "~"  # literal of current node
        self.is_word_end = False  # is there words ends in this node
        self.children = {}


def fill_BORtree(set_of_words):
    def add_word_to_bor(literals, bor):
        lt = literals.pop(0)
        if lt not in bor.children:
            bor.children[lt] = BORtree()

        bor.children[lt].is_word_end = not literals or bor.children[lt].is_word_end
        bor.children[lt].lit = lt

        if literals:
            add_word_to_bor(literals, bor.children[lt])

    root = BORtree()
    for word in set_of_words:
        literals = list(word)
        add_word_to_bor(literals, root)


# def find_closest_words_in_bor(word, bor, N_closest, alpha = 0.001):
#     words  = {}  # "global" variable
#     def go_down_the_bor(word_to_append, bor, error):
#
#
#     threshold = len(word) * alpha
#     i = 0
#     cur = bor
#     while i < len(word):


lm = LanguageModel()
lm.create_model("test.txt")
for word in lm.get_most_relevant_after_word("ая≥"):
    print(word)
