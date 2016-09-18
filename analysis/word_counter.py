import re
import os
from collections import Counter
import operator
import wikipedia


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

def get_word_counts(passages, stop_words=get_stop_words()):
	word_counts = Counter()
	total_words = 0

	for passage in passages:
		words = re.findall('\w+', passage)

		filtered_words = [word.lower() for word in words if word.lower() not in stop_words]

		word_counts += Counter(filtered_words)
		total_words += len(words)

	return word_counts, total_words


def get_most_patriotic():
	"""
	Checks which candidate uses the word America more often.
	"""
	candidates = ['hillary', 'trump']
	stop_words = get_stop_words()
	stop_words.remove('america')

	counters = {}

	for cand in candidates:
		counter, total_words = get_word_counts(get_passages_for_candidate(cand), stop_words=stop_words)

		america_count = 1.0*counter['america']/total_words

		counters[cand] = america_count
	print counters

	return max(counters.iteritems(), key=operator.itemgetter(1))[0]

def get_most_eloquent():
	"""
	Checks which candidate used SAT words more frequently.
	"""
	candidates = ['hillary', 'trump']

	with open('sat.txt') as f:
		sat_words = f.read().split()

	counters = {}

	for cand in candidates:
		counter, total_words = get_word_counts(get_passages_for_candidate(cand))

		for word in sat_words:
			eloquence_sum = 1.0*counter[word]/total_words
			try:
				counters[cand] += eloquence_sum
			except:
				counters[cand] = eloquence_sum
	print counters

	return max(counters.iteritems(), key=operator.itemgetter(1))[0]


def get_wikipedia_data():
	"""
	Gets the wikipedia content articles for Trump and Clinton
	"""
	trump = wikipedia.page("Donald_Trump").content.encode('utf-8')
	clinton = wikipedia.page("Hillary_Clinton").content.encode('utf-8')
	return {"trump": trump, "clinton": clinton}


def analyze_wikipedia_articles():
	"""
	Checks the most used words in describing Trump and Clinton
	"""
	data = get_wikipedia_data()
	most_common = {}

	for (cand, text) in data.iteritems():
		words = re.findall('\w+', text.lower())
		
		most_common[cand] = Counter(words).most_common(10)

	return most_common

print analyze_wikipedia_articles()
