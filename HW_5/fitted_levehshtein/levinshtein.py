from change_layout import switch_layout
from model_error import ErrorModel, bi_symbols


def generate_2gram_json():
    query_file = open("../queries_all.txt", "r")
    _bigram_distance = ErrorModel()
    for line in query_file:
        delimiter = line.find("\t")
        if delimiter == -1:
            continue
        # wrong = make_bigram(switch_layout(line[:delimiter].lower()))  # можно сделать лучше
        # right = make_bigram(line[delimiter + 1:-1].lower())
        # _bigram_distance.ne_fit(wrong, right)
        _bigram_distance.fit(bi_symbols(line[:delimiter].lower()),
                             bi_symbols(line[delimiter + 1:-1].lower()))
    _bigram_distance.prichesat_statistiku()

    _bigram_distance.store_json("statistics_2gram.json")
    query_file.close()


def generate_1gram_json():
    query_file = open("../queries_all.txt", "r")
    _ungram_distance = ErrorModel()
    for line in query_file:
        delimiter = line.find("\t")
        if delimiter == -1:
            continue
        _ungram_distance.fit(line[:delimiter].lower(),
                             line[delimiter + 1:-1].lower())
    _ungram_distance.prichesat_statistiku()

    _ungram_distance.store_json("statistics_1gram.json")
    query_file.close()


if __name__ == "__main__":
    # generate_2gram_json()
    generate_1gram_json()

    # класс, занющий статитстику по биграммам
    bigram_distance = ErrorModel()
    bigram_distance.load_json("statistics_1gram.json")

    import pprint

    pprint.pprint(bigram_distance.statistics)

    # er = ErrorStatistics()
    # er.ne_fit("мама", "рама")
    # er.store_json("t.json")
    # e = ErrorStatistics()
    # e.load_json("t.json")
    # print(e.get_weighted_distance("мама", "м"))
