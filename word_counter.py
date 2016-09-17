import re
from collections import Counter

filename = 'speeches/dnc-2016-obama-prepared-remarks.txt'

with open(filename) as f:
    passage = f.read()

words = re.findall(r'\w+', passage)

cap_words = [word.upper() for word in words]

word_counts = Counter(cap_words)

print word_counts.most_common(10)