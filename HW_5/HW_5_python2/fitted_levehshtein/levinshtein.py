# -*- coding: utf-8 -*-

from change_layout import switch_layout
from model_error import ErrorModel, bi_symbols, split

INPUT_FILE = "../queries_all.txt"
INPUT_FILE = "queries_all.txt"
# INPUT_FILE = "text.txt"



def generate_split_json(json_path):
    print('\033[93m' + "levenshtein generate_2gram_json()" + '\033[0m')
    query_file = open(INPUT_FILE, "r")
    _bigram_distance = ErrorModel()
    for line in query_file:
        delimiter = line.find("\t")
        if delimiter == -1:
            continue
        line = line.decode('utf-8')
        line = switch_layout(line)
        wrong = split(line[:delimiter].lower())
        right = split(line[delimiter + 1:-1].lower())
        if len(wrong) != len(right):  # произошел join или split
            continue
        for i in range(len(wrong)):  # для каждого слова
            _bigram_distance.fit(bi_symbols(wrong[i]), bi_symbols(right[i]))

    _bigram_distance.prichesat_statistiku()

    _bigram_distance.store_json(json_path)
    query_file.close()


def generate_2gram_json(json_path):
    print('\033[93m' + "levenshtein generate_2gram_json()" + '\033[0m')
    query_file = open(INPUT_FILE, "r")
    _bigram_distance = ErrorModel()
    for line in query_file:
        delimiter = line.find("\t")
        if delimiter == -1:
            continue
        line = line.decode('utf-8')
        line = switch_layout(line)
        wrong = split(line[:delimiter].lower())
        right = split(line[delimiter + 1:-1].lower())
        if len(wrong) != len(right):  # произошел join или split
            continue
        for i in range(len(wrong)):  # для каждого слова
            _bigram_distance.fit(bi_symbols(wrong[i]), bi_symbols(right[i]))

    _bigram_distance.prichesat_statistiku()

    _bigram_distance.store_json(json_path)
    query_file.close()


def generate_1gram_json(json_path):
    print('\033[93m' + "levenshtein generate_1gram_json()" + '\033[0m')
    query_file = open(INPUT_FILE, "r")
    _ungram_distance = ErrorModel()
    for line in query_file:
        line = line.decode('utf-8')
        delimiter = line.find("\t")
        if delimiter == -1:
            continue
        line = switch_layout(line)
        wrong = split(line[:delimiter].lower())
        right = split(line[delimiter + 1:-1].lower())
        if len(wrong) != len(right):  # произошел join или split
            continue
        for i in range(len(wrong)):  # для каждого слова
            _ungram_distance.fit(wrong[i], right[i])

    _ungram_distance.prichesat_statistiku()

    _ungram_distance.store_json(json_path)
    query_file.close()


if __name__ == "__main__":
    generate_2gram_json("statistics_2gram.json")
    generate_1gram_json("statistics_1gram.json")

    # класс, занющий статитстику по биграммам
    bigram_distance = ErrorModel()
    bigram_distance.load_json("statistics_2gram.json")

    import pprint

    fil = open("t.txt", "w")
    pprint.pprint(bigram_distance.statistics, fil)
    fil.close()

    # er = ErrorStatistics()
    # er.ne_fit("мама", "рама")
    # er.store_json("t.json")
    # e = ErrorStatistics()
    # e.load_json("t.json")
    # print(e.get_weighted_distance("мама", "м"))
