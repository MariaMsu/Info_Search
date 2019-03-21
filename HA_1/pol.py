import re
from urlparse import urlparse, parse_qs

import extract_features

extract_features.extract_features("f1.txt", "f2.txt", "out.txt")

a = u'123'
print a.isdigit()
