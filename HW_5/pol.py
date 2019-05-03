from bor_tree import BORtree

t = BORtree()

t.load_json("fitted_tree/tree.json")


for i in t.find_best("кошка"):
    print(i)
