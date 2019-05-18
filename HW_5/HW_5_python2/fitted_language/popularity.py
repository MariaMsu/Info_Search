# -*- coding: utf-8 -*-

from change_layout import switch_layout
from model_language import LanguageModel, split, create_pair_from_list

INPUT_FILE = "../queries_all.txt"
INPUT_FILE = "queries_all.txt"
# INPUT_FILE = "text.txt"

ungram_len = -1
bigram_len = -1


def generate_1gram_json(json_path):
    print('\033[93m' + "language generate_1gram_json()" + '\033[0m')
    query_file = open(INPUT_FILE, "r")
    _ungram_pop = LanguageModel()
    for line in query_file:
        if not line:
            continue
        line = line.decode('utf-8')
        delimiter = line.find("\t")
        _ungram_pop.fit(split(switch_layout(line[delimiter + 1:-1].lower())))

    _ungram_pop.prichesat_statistiku(cut_off=(1 / 1000000))  # переходим к вероятностям и отбрасываем редки слова

    _ungram_pop.store_json(json_path)
    global ungram_len
    ungram_len = len(_ungram_pop.dictionary)
    query_file.close()


def generate_2gram_json(json_path):
    print('\033[93m' + "language generate_2gram_json()" + '\033[0m')
    query_file = open(INPUT_FILE, "r")
    _bigram_pop = LanguageModel()
    for line in query_file:
        if not line:
            continue
        line = line.decode('utf-8')
        delimiter = line.find("\t")
        a = create_pair_from_list(split(switch_layout(line[delimiter + 1:-1].lower())))
        _bigram_pop.fit(a)

        # _bigram_pop.fit(create_pair_from_list(split(switch_layout(line[delimiter + 1:-1].lower()))))

    _bigram_pop.prichesat_statistiku(cut_off=(1 / 10000000))  # переходим к вероятностям и отбрасываем редки слова

    _bigram_pop.store_json(json_path)
    global bigram_len
    bigram_len = len(_bigram_pop.dictionary)
    query_file.close()


def info():
    print("INFO 1grma language word number: {}".format(ungram_len))
    print("INFO 2grma language word number: {}".format(bigram_len))


if __name__ == "__main__":
    generate_1gram_json("statistics_1gram.json")
    # generate_2gram_json("statistics_2gram.json")

    # класс, занющий статитстику

    pop = LanguageModel()
    pop.load_json("statistics_1gram.json")

    import pprint

    pprint.pprint(pop.dictionary)
    f = open("t1.txt", "w")
    pprint.pprint(pop.dictionary, f)
    f.close()

    # print("word number: {}".format(len(pop.dictionary)))
    print(info())


# word number ungram: 360303 - без обрезания непопулярных
# word number ungram: 62367 - cut
# word number bigram: 2018261 - без обрезания непопулярных?
# word number bigram: 2191650 - cut 1 / 1000000
# 2089815