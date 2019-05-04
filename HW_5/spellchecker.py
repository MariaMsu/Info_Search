from bor_tree import BORtree
from change_layout import switch_layout
from model_error import ErrorModel, bi_symbols
from model_language import LanguageModel

LOOP = 10
ALPHA = 0.5
bigram_distance = ErrorModel()
bigram_distance.load_json("fitted_levehshtein/statistics_2gram.json")

bigram_words = LanguageModel()
bigram_words.load_json("fitted_language/statistics_2gram.json")


def fix_score(_orig, _fix):
    def get_query_prob(query_list):
        len_words = len(query_list)
        prob = 1
        for i in range(len_words - 1):
            prob *= bigram_words.get_popularity(query_list[i] + query[i + 1])
        return prob

    def P_orig_fix():
        lev = bigram_distance.get_weighted_distance(bi_symbols(_orig), bi_symbols(_fix))
        return ALPHA ** (-lev)

    return P_orig_fix() * get_query_prob(_fix) / get_query_prob(_orig)


def generate_fix_query(st_matrix):
    query_dict = {0.1: "", 0.2: "", 0.3: "", 0.4: "", 0.5: ""}

    def get_word_chain(string, score, index):
        if score > max(query_dict):
            return
        if index - 1 >= len(st_matrix):
            query_dict[score] = string
            return
        for item in st_matrix[index]:
            print(string + [item])
            print(bigram_words.get_popularity(str(st_matrix[index][0]) + str(st_matrix[index + 1][0])))
            print(st_matrix[index][1])
            print(index + 1)
            get_word_chain(string + [item],
                           bigram_words.get_popularity(str(st_matrix[index][0]) + str(st_matrix[index + 1][0]))
                           + st_matrix[index][1],
                           index + 1)

    get_word_chain([], 0, 0)
    return query_dict


print("enter:\n")
bor = BORtree()
bor.load_json("fitted_tree/tree.json")
QUERY_VARIANTS = 5
WORD_VARIANTS = 5
while True:
    query = input()
    query = switch_layout(query)

    words_list = query.split(" ")
    variants = [("^", 0)]
    for word in words_list:
        var_list = bor.find_best(word)[:WORD_VARIANTS]
        variants += [var_list]
    variants += [("_", 0)]

    print(variants)
    best_query = ""
    max_score = 0
    for variant in generate_fix_query(variants):
        score = fix_score(query, variants)
        if score > max_score:
            max_score = score
            best_query = variant

    print(best_query[1:-1])

# todo caps
# vfvf b gfgf
