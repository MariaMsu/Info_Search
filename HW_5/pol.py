from bor_tree import BORtree
import numpy as np


def check():
    t = BORtree()

    t.load_json("fitted_tree/tree.json")

    for i in t.find_best("кошка"):
        print(i)


# check()

a = np.array([10, 20, 30])
b = np.array([[1, 2, 3]])
print(a / b)

# todo get_gram_statistics make return 0, not 1
