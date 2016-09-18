import re
from collections import Counter

filename = 'speeches/dnc-2016-obama-prepared-remarks.txt'

with open(filename) as f:
    passage = f.read()

with open('stop_words.txt') as f:
	stop_words = f.read().split()

words = re.findall(r'\w+', passage)

filtered_words = [word.lower() for word in words if word.lower() not in stop_words]


word_counts = Counter(filtered_words)

print word_counts.most_common(10)