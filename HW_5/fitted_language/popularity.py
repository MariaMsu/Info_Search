from model_language import LanguageModel, bi_word, split

INPUT_FILE = "../queries_all.txt"
# INPUT_FILE = "queries_all.txt"
# INPUT_FILE = "text.txt"

ungram_len = 0
bigram_len = 0


def generate_1gram_json(json_path):
    print('\033[93m' + "language generate_1gram_json()" + '\033[0m')
    query_file = open(INPUT_FILE, "r")
    _ungram_pop = LanguageModel()
    for line in query_file:
        if not line:
            continue
        delimiter = line.find("\t")
        _ungram_pop.fit(split(line[delimiter + 1:-1].lower()))

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
        delimiter = line.find("\t")
        _bigram_pop.fit(bi_word(line[delimiter + 1:-1].lower()))

    _bigram_pop.prichesat_statistiku(cut_off=(1 / 10000000))  # переходим к вероятностям и отбрасываем редки слова

    _bigram_pop.store_json(json_path)
    global bigram_len
    bigram_len = len(_bigram_pop.dictionary)
    query_file.close()


def info():
    print("INFO 1grma language word number: {}".format(ungram_len))
    print("INFO 2grma language word number: {}".format(bigram_len))


if __name__ == "__main__":
    # generate_1gram_json("statistics_1gram.json"))
    generate_2gram_json("statistics_2gram.json")

    # класс, занющий статитстику

    pop = LanguageModel()
    pop.load_json("statistics_1gram.json")

    import pprint

    pprint.pprint(pop.dictionary)
    f = open("t1.txt", "w")
    pprint.pprint(pop.dictionary, f)
    f.close()

    print("word number: {}".format(len(pop.dictionary)))

# word number ungram: 360303 - без обрезания непопулярных
# word number bigram: 2018261 - без обрезания непопулярных
# word number bigram: 2018261 - cut
