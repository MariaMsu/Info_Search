# coding: utf-8
import random
import re
import sys
from string import digits
from urlparse import urlparse, parse_qs, unquote

LINK_QUANTITY = 1000
ALPHA = 0.1


# INPUT_FILE_1 - Q_Link
def extract_features(INPUT_FILE_1, INPUT_FILE_2, OUTPUT_FILE):
    # 1 len :
    segments = {}

    # 2 mane_list :
    param_name = {}

    # 3 "param=value" :
    param = {}

    # 4a (index, name) :
    segment_name = {}

    # 4b index : 1
    segment_0_9 = {}

    # 4c (index, string) :
    segment_substr_0_9 = {}

    # 4d (index,  extension) :
    segment_ext = {}

    # todo 4e

    # 4d (index,  len) :
    segment_len = {}

    def _add_feature(dict_name, key):
        dict_name.setdefault(key, 0)
        dict_name[key] += 1

    def get_link_features(link):
        parse_list = urlparse(link)
        path = parse_list.path
        if path[0] == "/":
            path = path[1:]
        if len(path) > 0 and path[-1] == "/":
            path = path[:-1]
        segment_names_list = path.split("/")

        segments_number = len(segment_names_list)
        _add_feature(segments, segments_number)

        query_dict = parse_qs(parse_list.query)
        # not empty
        if query_dict:
            _add_feature(param_name, str(query_dict.keys()))

            for query in query_dict.items():
                _add_feature(param, "{}={}".format(query[0], query[1]))

        for number, segment in enumerate(segment_names_list):
            _add_feature(segment_name, (number, segment))
            _add_feature(segment_len, (number, len(segment)))
            if segment.find("%") >= 0:
                try:
                    segment = unquote(segment).decode("cp1251")
                except:
                    pass
            if segment.isdigit():
                _add_feature(segment_0_9, number)
            elif len(re.findall(r'\d+', segment)) == 1:
                _add_feature(segment_substr_0_9, number)

        last_segment_split = segment_names_list[-1].split(".")
        if len(last_segment_split) > 1:
            _add_feature(segment_ext, (segments_number - 1, last_segment_split[-1].lower()))

    def print_to_file():
        threshold = LINK_QUANTITY * ALPHA
        sort_features_dict = {}
        # 1
        for feature, number in segments.items():
            if number >= threshold:
                sort_features_dict["segments:{}\t{}".format(feature, number)] = number
        # 2
        for feature, number in param_name.items():
            if number >= threshold:
                sort_features_dict["param_name:{}\t{}".format(feature, number)] = number
        # 3
        for feature, number in param.items():
            if number >= threshold:
                sort_features_dict["param:{}\t{}".format(feature, number)] = number
        # 4a
        for feature, number in segment_name.items():
            if number >= threshold:
                sort_features_dict["segment_name_{}:{}\t{}".format(feature[0], feature[1], number)] = number
        # 4b
        for feature, number in segment_0_9.items():
            if number >= threshold:
                sort_features_dict["segment_[0-9]_{}:1\t{}".format(feature, number)] = number
        # 4c
        for feature, number in segment_substr_0_9.items():
            if number >= threshold:
                sort_features_dict["segment_substr[0-9]_{}:1\t{}".format(feature, number)] = number
        # 4d
        for feature, number in segment_ext.items():
            if number >= threshold:
                sort_features_dict["segment_ext_{}:{}\t{}".format(feature[0], feature[1], number)] = number
        # 4f
        for feature, number in segment_len.items():
            if number >= threshold:
                sort_features_dict["segment_len_{}:{}\t{}".format(feature[0], feature[1], number)] = number

        sort_features_dict = sorted(sort_features_dict, key=sort_features_dict.get, reverse=True)
        for feature in sort_features_dict:
            out.write(feature + '\n')

    def load_links(file, quantity):
        loaded = 0
        while loaded < quantity:
            step = random.randint(1, 5)
            for number, line in enumerate(file):
                if number % step != 0:
                    continue
                get_link_features(line[:-1])
                loaded += 1
                if loaded >= quantity:
                    break
            file.seek(0)

    q_link = open(INPUT_FILE_1, "r")
    all_link = open(INPUT_FILE_2, "r")
    out = open(OUTPUT_FILE, "w")

    load_links(q_link, LINK_QUANTITY)
    load_links(all_link, LINK_QUANTITY)
    print_to_file()

    q_link.close()
    all_link.close()
    out.close()
