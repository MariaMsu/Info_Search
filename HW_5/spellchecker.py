import math

from bor_tree import BORtree
from change_layout import switch_layout
from model_error import ErrorModel
from model_language import LanguageModel, bi_word

LOOP = 10
ALPHA = 0.5
REFLECT_POW = 1 / 5  # для отображения маленьких чисел в числа побольше
bigram_distance = ErrorModel()
bigram_distance.load_json("fitted_levehshtein/statistics_2gram.json")

bigram_words = LanguageModel()
bigram_words.load_json("fitted_language/statistics_2gram.json")


def fix_score(_fix, distance, orig_popularity):
    _fix_bigram = []
    for i in range(len(_fix) - 1):
        _fix_bigram += [_fix[i] + _fix[i + 1]]

    def get_query_pop():
        prob = 1
        for bigram in _fix_bigram:
            print("bi-word distance {} = {}".format(bigram, bigram_words.get_popularity(bigram) ** REFLECT_POW))
            prob *= bigram_words.get_popularity(bigram) ** REFLECT_POW
        return prob

    print("{}: ---> P(orig|fix)={}, fix_pop={}, orig_pop={} |--> result={}".format(_fix,
                                                                                   ALPHA * distance,
                                                                                   get_query_pop(),
                                                                                   orig_popularity,
                                                                                   ALPHA * distance * get_query_pop() / orig_popularity))
    return ALPHA * distance * get_query_pop() / orig_popularity


def query_str_popularity(str):
    pop = 1
    query_bigram = bi_word(str)
    for bigram in query_bigram:
        print("! bi-word distance {} = {}".format(bigram, bigram_words.get_popularity(bigram) ** REFLECT_POW))
        pop *= bigram_words.get_popularity(bigram) ** REFLECT_POW
    return pop


# example matrix:
# [[('^', 0)],
# [('мама', 72.98082350632582), ('ама', 0.5383555445372121), ('мае', 0.10552840027246843),
# ('она', 0.06729444306715152), ('маме', 0.04638222569967016)],
# [('и', 10117.719515146231), ('е', 0.24201797706468076), ('ы', 0.09304246673819949)],
# [('папа', 29.306729955744483), ('про', 1.0906063007601103), ('пепа', 0.14960278578275116),
# ('анапа', 0.057049617406182175), ('лапа', 0.05228054341870336)], [('_', 0)]]
def generate_fix_query(st_matrix):
    query_dict = {}

    min_key = 0

    def add_query(local_score, string):
        # находим цепочки с наибольшим score'ом
        nonlocal min_key
        if len(query_dict) <= QUERY_VARIANTS:
            query_dict[local_score] = string
            return
        if local_score < min_key:
            return
        min_key = min(query_dict)
        query_dict.pop(min_key)
        query_dict[local_score] = string

    def get_word_chain(string, local_score, index):
        # if local_score > min_key:
        #     print("-----------ABORT-------- {}".format(string))
        #     return
        if index + 1 >= len(st_matrix):
            # print("score {}, string {}".format(score, string + [st_matrix[-1][0][0]]))
            # string+st_matrix[index] = "_"
            add_query(local_score, string + [st_matrix[-1][0][0]])
            return
        for item in st_matrix[index]:
            # print("1 item {}".format(item))
            # print("2 list string {}".format(string + [item[0]]))
            # # if index - 1 >= len(st_matrix):
            # print("3 pop strings {} --- {}".format(st_matrix[index][0][0], st_matrix[index + 1][0][0]))
            # print("4 cur popular {}, old popular {}".
            #       format(local_score
            #              + bigram_words.get_popularity(str(st_matrix[index][0][0]) + str(st_matrix[index + 1][0][0]))
            #              ** REFLECT_POW + item[1],
            #              local_score))
            # print("5 score {}".format(item[1]))
            # print("6 new index {}".format(index + 1))
            get_word_chain(string + [item[0]],

                           local_score
                           + bigram_words.get_popularity(str(st_matrix[index][0][0]) + str(st_matrix[index + 1][0][0]))
                           ** REFLECT_POW
                           + item[1],

                           index + 1)

    get_word_chain([], 0, 0)
    return query_dict


bor = BORtree()
bor.load_json("fitted_tree/tree.json")
QUERY_VARIANTS = 5
WORD_VARIANTS = 5
while True:
    print("enter:")
    query = input()
    query = switch_layout(query)

    words_list = query.split(" ")
    variants = [[("^", 0)]]
    for word in words_list:
        var_list = bor.find_best(word)[:WORD_VARIANTS]
        variants += [var_list]
        print("=====================================================")
    variants += [[("_", 0)]]

    print(variants)
    best_query = ""
    max_score = 0
    a = generate_fix_query(variants)
    print("variant matrix: " + str(a))
    query_popularity = query_str_popularity(query)
    for key, one_variant in a.items():
        score = fix_score(_fix=one_variant, distance=key, orig_popularity=query_popularity)
        if score > max_score:
            max_score = score
            best_query = one_variant

    print(best_query)
    print(' '.join(best_query[1:-1]))

# todo caps
