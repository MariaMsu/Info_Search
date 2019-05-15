from fitted_language import popularity
from fitted_levehshtein import levinshtein
from fitted_tree import tree

levinshtein.generate_1gram_json("fitted_levehshtein/statistics_1gram.json")
levinshtein.generate_2gram_json("fitted_levehshtein/statistics_2gram.json")


popularity.generate_1gram_json("fitted_language/statistics_1gram.json")
popularity.generate_2gram_json("fitted_language/statistics_2gram.json")
popularity.info()

tree.generate_tree_json("fitted_tree/tree.json")
