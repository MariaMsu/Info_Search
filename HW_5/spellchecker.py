import json

from bor_tree import BORtree
from change_layout import switch_layout
from model_error import ErrorModel, bi_symbols

LOOP = 10
ALPHA = 0.5
bigram_distance = ErrorModel()
bigram_distance.load_json("fitted_levehshtein/statistics_2gram.json")


def fix_score(_orig, _fix):
    global bigram_distance

    def P_orig_fix():
        lev = bigram_distance.get_weighted_distance(bi_symbols(_orig), bi_symbols(_fix))
        return ALPHA ** (-lev)

    def P_orig():
        pass

    def P_fix():
        pass

    return P_orig_fix() * P_fix() / P_orig()

def generate_fix_query(string_matrix):
    query_list = []


print("enter:\n")
bor = BORtree()
bor.load_json("fitted_tree/tree.json")
DEFAULT_SCORE = 100
while True:
    query = input()
    query = switch_layout(query)

    words_list = query.split(" ")
    variants = []
    for word in words_list:
        var_list = [(word, DEFAULT_SCORE)] + bor.best_matches(word)
        variants += [var_list]


    print(query)

# orig_query = sys.argv[1]
# query = switch_layout(orig_query).lower()  # смена раскладки
# fix_variants = {query}
# fix = ""
# for _ in range(LOOP):
#     fix = bor(fix)
#     if len(fix_variants & fix) > 0:
#         break
#     fix_variants.add(fix)
#
# best = (fix, fix_score(orig_query, fix))
# for variant in fix_variants:
#     score = fix_score(orig_query, variant)
#     if score > best[1]:
#         best = (variant, score)
#
# print(best[0])
