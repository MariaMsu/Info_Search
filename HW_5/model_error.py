import numpy as np
import json

EMPTY_LEX = "~"
MAX_WORD_LEN = 15
DEFAULT_ERROR = 0.5 / 100
SPECIAL_LEX = {"_", "-", "—", "'"}


def split(string):
    word_list = []
    word = str()
    for char in string:
        if ("A" <= char <= "Z") or \
                ("a" <= char <= "z") or \
                ("А" <= char <= "Я") or \
                ("а" <= char <= "я") or \
                (char in SPECIAL_LEX):
            word += char
        elif word:
            if len(word) < MAX_WORD_LEN:
                word_list += [word]
            word = str()
    if word:
        word_list += [word]
    return word_list


class ErrorModel:
    def __init__(self):
        self.statistics = dict()  # {"origin" : {"fix" : number}}
        self._statistics_size = 0

    def load_json(self, json_path):
        (size, stat) = json.loads(open(json_path, "r").read())
        self._statistics_size, self.statistics = size, stat

    def store_json(self, json_path):
        file = open(json_path, "w")
        file.write(json.dumps((self._statistics_size, self.statistics)))
        file.close()

    def fit(self, a, b):
        levenshtein_matrix = self._get_levenshtein_matrix(a, b)
        self._fill_statistics(a, b, levenshtein_matrix)

    def prichesat_statistiku(self):
        for orig in self.statistics.keys():
            replace_count = 0
            for fix in self.statistics[orig].keys():
                replace_count += self.statistics[orig][fix]
            for fix in self.statistics[orig].keys():
                self.statistics[orig][fix] /= replace_count

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
                possible_actions = np.array([(previous_row[j - 1] + int(a[j - 1] != b[i - 1])),  # change
                                             (previous_row[j] + 1),  # add
                                             (current_row[j - 1] + 1)])  # delete
                weight_mask = np.array([self.get_popularity(a[j - 1], b[i - 1]),  # change
                                        self.get_popularity(EMPTY_LEX, b[i - 1]),  # add
                                        self.get_popularity(a[j - 1], EMPTY_LEX)])  # delete
                weighted_action = possible_actions + (1 / weight_mask)
                action = np.argmin(weighted_action)
                current_row[j] = weighted_action[action.item()]
            # matrix = np.vstack((matrix, [current_row]))
            # print(str(a) + " -- " + str(b))
            # print(matrix)
        return current_row[n]

    # return (кол-во вхождений этой замены некоторого элемента / кол-во всех замен этого элемента)
    def get_popularity(self, orig, fix):
        if orig == fix:  # warning! di not call in this case, return 0 manually
            # print("error {}".format(0))
            return 1
        if (orig in self.statistics) and (fix in self.statistics[orig]):
            # print("error {}".format(self.statistics[orig][fix]))
            return self.statistics[orig][fix]
        # print("error {}".format(1 / 1000))
        return DEFAULT_ERROR  # TODO flexible (newer sow this case)

    def _add_statistics(self, orig, fix):
        self.statistics.setdefault(orig, dict())
        self.statistics[orig].setdefault(fix, 0)
        self.statistics[orig][fix] += 1
        self._statistics_size += 1

    def _fill_statistics(self, a, b, matrix):
        n, m = len(a), len(b)
        MAX_DISTANCE = (n + 1) * (m + 1)

        position = [n, m, matrix[m, n]]  # [x, y, distance]
        while position[2] != 0:  # пока distance не станет 0
            x, y = position[0], position[1]

            # только один из возможных путей изменения. можно сделать лучше
            possible_actions = [matrix[y - 1][x - 1] if (x > 0) and (y > 0) else MAX_DISTANCE,  # change
                                matrix[y - 1][x] if y > 0 else MAX_DISTANCE,  # add
                                matrix[y][x - 1] if x > 0 else MAX_DISTANCE]  # delete
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
                    self._add_statistics(EMPTY_LEX, b[y - 1])
                    #           self._add_statistics(a[x - 1][1] + EMPTY_LEX, b[y - 1]) #  only for bigram
                    # print("~ -> " + b[y - 1])
                position[1] -= 1
            else:  # delete
                if position[2] != possible_actions[action.item()]:
                    position[2] -= 1
                    self._add_statistics(a[x - 1], EMPTY_LEX)
                    #           self._add_statistics(a[x - 1], EMPTY_LEX + b[y - 1][1]) #  only for bigram
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


# represent word as bigrams
def bi_symbols(string):
    if not string:
        return []
        # return ["^_"]
    new_string = ["^" + string[0]]
    for i in range(len(string) - 1):
        new_string += [string[i:i + 2]]
    new_string += [string[-1:] + "_"]
    return new_string


if __name__ == "__main__":
    error = ErrorModel()
    error.load_json("fitted_levehshtein/statistics_2gram.json")
    a = "кшка"
    b = "кошка"

    # error.fit(bi_symbols(a), bi_symbols(b))
    print(error.statistics)
    print(error.get_weighted_distance(bi_symbols("ком"), bi_symbols("кот")))
