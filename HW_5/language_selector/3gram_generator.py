# input_file = "russian_example.txt"
# output_file = "russian.txt"

input_file = "english_example.txt"
output_file = "english.txt"

TOP_SIZE = 100
N_GRAM = 2


def dict_add(gr):
    gram.setdefault(gr, 0)
    gram[gr] += 1


file = open(input_file, "r")
gr_file = open(output_file, "w")
gram = dict()

for line in file:
    for word in line[:-1].lower().split(" "):
        for i in range(len(word) - (N_GRAM - 1)):
            dict_add(word[i:i + N_GRAM])

top_gram = sorted(gram.items(), key=lambda kv: kv[1], reverse=True)[:TOP_SIZE]

for i in top_gram:
    gr_file.write("\"{}\", ".format(i[0]))

gr_file.write("\nTOP {}".format(TOP_SIZE))
file.close()
gr_file.close()
