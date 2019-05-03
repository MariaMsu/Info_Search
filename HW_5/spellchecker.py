import sys
import json

from change_layout import switch_layout
from model_error import ErrorModel, make_bigram

LOOP = 10
ALPHA = 0.5
bigram_distance = ErrorModel()
bigram_distance.load_json("bigram_levehshtein/statistics.json")


def fix_score(_orig, _fix):
    global bigram_distance

    def P_orig_fix():
        lev = bigram_distance.get_weighted_distance(make_bigram(_orig), make_bigram(_fix))
        return ALPHA ** (-lev)

    def P_orig():
        pass

    def P_fix():
        pass

    return P_orig_fix() * P_fix() / P_orig()


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

a = "мама"
b = "кама"
print(bigram_distance.get_weighted_distance(make_bigram(a), make_bigram(b)))
a = "кропотов"
b = "пидор"
print(bigram_distance.get_weighted_distance(make_bigram(a), make_bigram(b)))
