# coding: utf-8

from sklearn.cluster import MeanShift
import re
import numpy as np
from urlparse import urlparse, parse_qs, unquote

ALPHA = 0.1

Cluster = None
Vector_map = None
Quota_list = None


def link_to_vector(vector_map, link):
    features_list = []
    parse_list = urlparse(link)
    path = parse_list.path
    if path[0] == "/":
        path = path[1:]
    if len(path) > 0 and path[-1] == "/":
        path = path[:-1]
    segment_names_list = path.split("/")

    segments_number = len(segment_names_list)
    features_list.append("segments:{}".format(segments_number))

    query_dict = parse_qs(parse_list.query)
    # not empty
    if query_dict:
        features_list.append("param_name:{}".format(str(query_dict.keys())))

        for query in query_dict.items():
            features_list.append("param:{}={}".format(query[0], query[1][0]))

    contain_digit = False
    for iteration, segment in enumerate(segment_names_list):
        contain_digit = False
        features_list.append("segment_name_{}:{}".format(iteration, segment))
        features_list.append("segment_len_{}:{}".format(iteration, len(segment)))
        if segment.find("%") >= 0:
            try:
                segment = unquote(segment).decode("cp1251")
            except:
                pass
        if segment.isdigit():
            features_list.append("segment_[0-9]_{}:1".format(iteration))
        elif len(re.findall(r'\d+', segment)) == 1:
            features_list.append("segment_substr[0-9]_{}:1".format(iteration))
            contain_digit = True

    last_segment_split = segment_names_list[-1].split(".")
    contain_ext = False
    if len(last_segment_split) > 1:
        features_list.append("segment_ext_{}:{}".format(segments_number - 1, last_segment_split[-1].lower()))
        contain_ext = True

    if contain_digit and contain_ext:
        # del segment_substr_0_9[segments_number - 1]
        # del segment_ext[(segments_number - 1, last_segment_split[-1].lower())]
        features_list.append("segment_ext_substr_[0-9]_{}:{}"
                             .format(segments_number - 1, last_segment_split[-1].lower()))

    features_list = sorted(features_list)
    feature_len = len(features_list)
    index = 0
    vector = np.zeros(len(vector_map))
    for iteration, feature in enumerate(sorted(vector_map)):
        while features_list[index] < feature:
            index += 1
            if index>=feature_len:
                break
        if features_list[index] == feature:
            vector[iteration] = 1
            continue
    return vector


def get_link_features(sekitei, link):
    def _add_feature(dict_name, key):
        dict_name.setdefault(key, 0)
        dict_name[key] += 1

    parse_list = urlparse(link)
    path = parse_list.path
    if path[0] == "/":
        path = path[1:]
    if len(path) > 0 and path[-1] == "/":
        path = path[:-1]
    segment_names_list = path.split("/")

    segments_number = len(segment_names_list)
    _add_feature(sekitei.segments, segments_number)

    query_dict = parse_qs(parse_list.query)
    # not empty
    if query_dict:
        _add_feature(sekitei.param_name, str(query_dict.keys()))

        for query in query_dict.items():
            _add_feature(sekitei.param, "{}={}".format(query[0], query[1][0]))

    contain_digit = False
    for number, segment in enumerate(segment_names_list):
        contain_digit = False
        _add_feature(sekitei.segment_name, (number, segment))
        _add_feature(sekitei.segment_len, (number, len(segment)))
        if segment.find("%") >= 0:
            try:
                segment = unquote(segment).decode("cp1251")
            except:
                pass
        if segment.isdigit():
            _add_feature(sekitei.segment_0_9, number)
        elif len(re.findall(r'\d+', segment)) == 1:
            _add_feature(sekitei.segment_substr_0_9, number)
            contain_digit = True

    last_segment_split = segment_names_list[-1].split(".")
    contain_ext = False
    if len(last_segment_split) > 1:
        _add_feature(sekitei.segment_ext, (segments_number - 1, last_segment_split[-1].lower()))
        contain_ext = True

    if contain_digit and contain_ext:
        # del segment_substr_0_9[segments_number - 1]
        # del segment_ext[(segments_number - 1, last_segment_split[-1].lower())]
        _add_feature(sekitei.segment_ext_substr_0_9, (segments_number - 1, last_segment_split[-1].lower()))


def create_vector_space(sekitei, threshold):
    features_list = []
    # 1
    for feature, number in sekitei.segments.items():
        if number > threshold:
            features_list.append("segments:{}".format(feature))
    # 2
    for feature, number in sekitei.param_name.items():
        if number > threshold:
            features_list.append("param_name:{}".format(feature))
    # 3
    for feature, number in sekitei.param.items():
        if number > threshold:
            features_list.append("param:{}".format(feature))
    # 4a
    for feature, number in sekitei.segment_name.items():
        if number > threshold:
            features_list.append("segment_name_{}:{}".format(feature[0], feature[1]))
    # 4b
    for feature, number in sekitei.segment_0_9.items():
        if number > threshold:
            features_list.append("segment_[0-9]_{}:1".format(feature))
    # 4c
    for feature, number in sekitei.segment_substr_0_9.items():
        if number > threshold:
            features_list.append("segment_substr[0-9]_{}:1".format(feature))
    # 4d
    for feature, number in sekitei.segment_ext.items():
        if number > threshold:
            features_list.append("segment_ext_{}:{}".format(feature[0], feature[1]))
    # 4e
    # for feature, number in sekitei.segment_ext_substr_0_9.items():
    #     if number > threshold:
    #         features_list.append("segment_ext_substr_[0-9]_{}:{}".format(feature[0], feature[1]))

    # 4f
    for feature, number in sekitei.segment_len.items():
        if number > threshold:
            features_list.append("segment_len_{}:{}".format(feature[0], feature[1]))

    return sorted(features_list)


class sekitei_data:

    def __init__(self):
        self.segments = {}  # 1 len :
        self.param_name = {}  # 2 mane_list :
        self.param = {}  # 3 "param=value" :
        self.segment_name = {}  # 4a (index, name) :
        self.segment_0_9 = {}  # 4b index : 1
        self.segment_substr_0_9 = {}  # 4c (index, string) :
        self.segment_ext = {}  # 4d (index,  extension) :
        self.segment_ext_substr_0_9 = {}  # 4e (index, string) :
        self.segment_len = {}  # 4f (index,  len) :


def define_segments(QLINK_URLS, UNKNOWN_URLS, QUOTA):
    major_data = sekitei_data()
    links_quantity = 0
    for link in QLINK_URLS:
        get_link_features(major_data, link)
        links_quantity += 1
    q_link_number = links_quantity
    for link in UNKNOWN_URLS:
        get_link_features(major_data, link)
        links_quantity += 1

    global Vector_map
    Vector_map = create_vector_space(major_data, links_quantity * ALPHA)
    major_matrix = np.empty([links_quantity, len(Vector_map)], dtype=int)

    index = 0
    for row in QLINK_URLS:
        major_matrix[index] = link_to_vector(Vector_map, row)
        index += 1
    for row in UNKNOWN_URLS:
        major_matrix[index] = link_to_vector(Vector_map, row)
        index += 1

    global Cluster
    global Quota_list
    Cluster = MeanShift(bandwidth=2.5).fit(major_matrix)
    Quota_list = np.ones(np.amax(Cluster.labels_)+1)
    print Cluster.labels_
    for q_cluster in Cluster.labels_[:q_link_number]:
        Quota_list[q_cluster] += 1
    Quota_list *= QUOTA / np.sum(Quota_list)


#
# returns True if need to fetch url
#
def fetch_url(url):
    global Cluster
    global Vector_map
    global Quota_list
    label = Cluster.predict([link_to_vector(Vector_map, url)])
    if Quota_list[label] > 0:
        Quota_list[label] -= 1
        return True
    return False
