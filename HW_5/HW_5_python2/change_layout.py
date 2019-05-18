# -*- coding: utf-8 -*-

import string

# меняем раскладку, если надо. для этого анализируем биграммы
# биграммы получены в language_selector

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

russian = {k.decode('utf-8') for k in russian}

en = u"qwertyuiop[]asdfghjkl;'zxcvbnm,.`" + u'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'
ru = u"йцукенгшщзхъфывапролджэячсмитьбюё" + u'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'
ru_to_en = {ord(c): ord(t) for c, t in zip(ru, en)}
en_to_ru = {ord(c): ord(t) for c, t in zip(en, ru)}

# ru_to_en = string.maketrans(ru, en)
# en_to_ru = string.maketrans(en, ru)

N_GRAM = 2

def switch_layout(string):
    new_str = string
    # print type(new_str)
    rus = new_str.translate(en_to_ru)
    new_str = string
    eng = new_str.translate(ru_to_en)
    rus_confidence = len(_get_3gram(rus) & russian)
    eng_confidence = len(_get_3gram(eng) & english)
    # print(str(rus_confidence) + " " + str(eng_confidence))
    return rus if rus_confidence >= eng_confidence else eng


def _get_3gram(string):
    new_set = set()
    for i in range(len(string) - (N_GRAM - 1)):
        new_set.add(string[i:i + N_GRAM])
    return new_set


if __name__ == "__main__":
    a = u"вшсл"
    print(switch_layout(a))

    # nummap = {ord(c): ord(t) for c, t in zip(u"qaz", u"йфя")}
    # new_str = u"1qd"
    # print new_str.translate(nummap)
