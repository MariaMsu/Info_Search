from bor_tree import BORtree
from model_language import LanguageModel


def generate_tree_json():
    tree = BORtree()
    pop = LanguageModel()
    pop.load_json("../fitted_language/statistics_1gram.json")
    for word in pop.dictionary:
        tree.fit(word)
    tree.store_json("tree.json")


if __name__ == "__main__":
    generate_tree_json()