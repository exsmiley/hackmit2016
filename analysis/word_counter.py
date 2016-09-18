import re
import os
from collections import Counter
import operator


def get_passages_for_candidate(person):
	passages = []

	filenames = map(lambda x: '%s/' % person + x, filter(lambda x: x != '.DS_Store', os.listdir(person)))

	for filename in filenames:
	    with open(filename) as f:
	        passages.append(f.read().decode('utf-8'))

	return passages

def get_stop_words():
	with open('stop_words.txt') as f:
		stop_words = f.read().split()
	return stop_words

def word_counts(passages, stop_words=get_stop_words()):
	word_counts = Counter()
	total_words = 0

	for passage in passages:
		words = re.findall(r'\w+', passage)

		filtered_words = [word.lower() for word in words if word.lower() not in stop_words]

		word_counts += Counter(filtered_words)
		total_words += len(words)

	return word_counts, total_words


def get_most_patriotic():
	candidates = ['hillary', 'trump', 'obama']
	stop_words = get_stop_words()
	stop_words.remove('america')

	counters = {}

	for cand in candidates:
		counter, total_words = word_counts(get_passages_for_candidate(cand), stop_words=stop_words)

		america_count = 1.0*counter['america']/total_words

		counters[cand] = america_count

	return max(counters.iteritems(), key=operator.itemgetter(1))[0]

print get_most_patriotic()
