# меняем раскладку, если надо. для этогго анализируем биграммы

english = {"th", "he", "an", "nd", "in", "er", "ha", "re", "of", "or", "hi", "at", "ou", "en", "to", "al", "is", "ll",
           "on", "it", "es", "se", "nt", "ed", "ve", "ar", "sh", "ng", "ea", "ho", "st", "me", "be", "le", "as", "fo",
           "ne", "un", "te", "sa", "lo", "wi", "rd", "ai", "no", "il", "et", "ri", "el", "ro", "wh", "de", "ch", "ma",
           "om", "d,", "us", "ee", "em", "ut", "ot", "so", ":1", "am", "we", "co", "wa", "s,", "ur", "id", "im", "ra",
           "ay", "e,", "ey", "ca", "ke", "ld", "ti", "go", "ce", "la", "ir", "ow", "ns", "av", "li", "gh", "mo", "ad",
           "ic", "ei", "rs", "da", ":2", "ye", "od", "ie", "pe", "ss"}

russian = {"но", "ст", "ра", "на", "ро", "то", "ал", "ов", "пр", "не", "по", "го", "ко", "ор", "ва", "ос", "ен", "ре",
           "ны", "та", "ни", "ом", "ли", "ел", "ль", "ав", "ка", "ол", "ер", "ан", "ин", "ат", "де", "ог", "во", "ми",
           "ый", "ем", "ла", "те", "он", "ес", "от", "со", "ск", "да", "ил", "ве", "ас", "ит", "ть", "ло", "и,", "ак",
           "ди", "од", "ам", "ри", "ле", "ет", "мо", "ти", "тр", "за", "ой", "ки", "нн", "ви", "ру", "ся", "об", "ар",
           "же", "че", "бо", "ег", "се", "ий", "им", "до", "кр", "ез", "вы", "ме", "из", "ьн", "га", "ик", "ма", "ым",
           "ши", "лс", "ей", "тв", "ир", "ис", "ул", "бе", "ци", "их"}

en = "qwertyuiop[]asdfghjkl;'zxcvbnm,.`" + 'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'
ru = "йцукенгшщзхъфывапролджэячсмитьбюё" + 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'
ru_to_en = str.maketrans(ru, en)
en_to_ru = str.maketrans(en, ru)

N_GRAM = 2


def switch_layout(string):
    new_str = string
    rus = new_str.translate(en_to_ru)
    new_str = string
    eng = new_str.translate(ru_to_en)
    rus_confidence = len(_get_3gram(rus) & russian)
    eng_confidence = len(_get_3gram(eng) & english)
    print(str(rus_confidence) + " " + str(eng_confidence))
    return rus if rus_confidence >= eng_confidence else eng


def _get_3gram(string):
    new_set = set()
    for i in range(len(string) - (N_GRAM - 1)):
        new_set.add(string[i:i + N_GRAM])
    return new_set


print(switch_layout("fyyfcbvbyjdbx"))
