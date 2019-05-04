from bor_tree import BORtree
import numpy as np


def check():
    t = BORtree()

    t.load_json("fitted_tree/tree.json")

    for i in t.find_best("кошка"):
        print(i)


# check()

a = [1, 2, 3, 4]
print(a[1:-1])

# todo get_gram_statistics make return 0, not 1
