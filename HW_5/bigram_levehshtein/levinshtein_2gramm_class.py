from change_layout import switch_layout
from model_error import ErrorModel, make_bigram


def generate_json():
    query_file = open("queries_all.txt", "r")
    _bigram_distance = ErrorModel()
    for line in query_file:
        delimiter = line.find("	")
        if delimiter == -1:
            continue
        # wrong = make_bigram(switch_layout(line[:delimiter].lower()))  # можно сделать лучше
        # right = make_bigram(line[delimiter + 1:-1].lower())
        # _bigram_distance.ne_fit(wrong, right)
        _bigram_distance.ne_fit(make_bigram(line[:delimiter].lower()),
                                make_bigram(line[delimiter + 1:-1].lower()))
    _bigram_distance.prichesat_statistiku()

    _bigram_distance.store_json("statistics.json")
    query_file.close()


if __name__ == "__main__":
    generate_json()

    # класс, занющий статитстику по биграммам
    bigram_distance = ErrorModel()
    bigram_distance.load_json("statistics.json")

    import pprint

    pprint.pprint(bigram_distance.statistics)

    # er = ErrorStatistics()
    # er.ne_fit("мама", "рама")
    # er.store_json("t.json")
    # e = ErrorStatistics()
    # e.load_json("t.json")
    # print(e.get_weighted_distance("мама", "м"))
