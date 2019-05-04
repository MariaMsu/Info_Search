from bor_tree import BORtree
import bor_tree
from model_language import LanguageModel


def generate_tree_json(json_path):
    print('\033[93m' + "tree generate_tree_json()" + '\033[0m')
    tree = BORtree()
    pop = LanguageModel()
    pop.load_json(bor_tree.PREFIX_PATH + "fitted_language/statistics_1gram.json")
    for word in pop.dictionary:
        tree.fit(word)
    tree.store_json(json_path)


if __name__ == "__main__":
    bor_tree.PREFIX_PATH = "../"  # изменение путей к json'ам

    generate_tree_json("tree.json")

    tree = BORtree()
    tree.load_json("tree.json")
    # tree.fit("кот")
    # tree.fit("кошка")
    # tree.fit("пыль")
    # tree.fit("конопля")

    f = open("t1.txt", "w")


    def print_words(_tree, node=0, word=""):
        word += _tree[node][0]
        if _tree[node][0] == '\n':
            f.write(word)
            return
        for key, value in _tree[node][1].items():
            print_words(_tree, value, word)


    print_words(tree.tree)
    f.close()
