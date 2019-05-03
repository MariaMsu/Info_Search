from model_language import LanguageModel, bi_word, split


def generate_1gram_json():
    query_file = open("../queries_all.txt", "r")
    _ungram_pop = LanguageModel()
    for line in query_file:
        delimiter = line.find("\t")
        _ungram_pop.fit(split(line[delimiter + 1:-1].lower()))

    _ungram_pop.prichesat_statistiku()

    _ungram_pop.store_json("statistics_1gram.json")
    query_file.close()


def generate_2gram_json():
    query_file = open("../queries_all.txt", "r")
    _ungram_pop = LanguageModel()
    for line in query_file:
        delimiter = line.find("\t")
        _ungram_pop.fit(bi_word(line[delimiter + 1:-1].lower()))

    _ungram_pop.prichesat_statistiku()

    _ungram_pop.store_json("statistics_2gram.json")
    query_file.close()


if __name__ == "__main__":
    generate_1gram_json()
    generate_2gram_json()

    # класс, занющий статитстику

    pop = LanguageModel()
    pop.load_json("statistics_1gram.json")

    import pprint

    pprint.pprint(pop.dictionary)
    f = open("t1.txt", "w")
    pprint.pprint(pop.dictionary, f)
    f.close()
