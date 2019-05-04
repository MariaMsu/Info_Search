from bor_tree import BORtree


def check():
    t = BORtree()

    t.load_json("fitted_tree/tree.json")

    for i in t.find_best("кошка"):
        print(i)


check()
