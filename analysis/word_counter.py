import re
import os
from collections import Counter
import operator
import wikipedia
import string
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


def get_passages_for_candidate(person):
    passages = []

    filenames = map(lambda x: '%s/' % person + x, filter(lambda x: x != '.DS_Store', os.listdir(person)))

    for filename in filenames:
        with open(filename) as f:
            passages.append(f.read().decode('utf-8'))

    return passages

def get_stop_words():
    """
    List of stop words
    @return list of stop words
    """
    with open('stop_words.txt') as f:
        stop_words = f.read().split()
    return stop_words

def get_word_counts(passages, stop_words=get_stop_words()):
    """
    Counts all of the word frequencies of words in the passages
    @return Counter of the words
    """
    word_counts = Counter()
    total_words = 0

    for passage in passages:
        words = re.findall(r'\w+', passage.lower())

        filtered_words = [word for word in words if word not in stop_words]

        word_counts = Counter(filtered_words)
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
    printable = set(string.printable)
    trump = filter(lambda x: x in printable, trump)
    clinton = filter(lambda x: x in printable, clinton)
    return {"trump": trump, "clinton": clinton}


def analyze_wikipedia_articles():
    """
    Checks the most used words in describing Trump and Clinton
    """
    data = get_wikipedia_data()
    most_common = {}

    for (cand, text) in data.iteritems():
        most_common[cand] = get_word_counts(text)[0]
        words = re.findall('\w+', text.lower())
        
        most_common[cand] = Counter(words).most_common(10)

    return most_common


def wikipedia_sentiment_analysis():
    """
    Gets the sentiment for each of the candidates' wikipedia articles
    @return dict of {cand: sentiment dict}
    """
    data = get_wikipedia_data()
    results = {}

    for cand in data.keys():
        lines_list = tokenize.sent_tokenize(data[cand])
        sid = SentimentIntensityAnalyzer()
        polarity_score = {"neg": 0, 'neu': 0, 'pos': 0, 'compound': 0}
        for sentence in lines_list:
            # print sentence
            ss = sid.polarity_scores(sentence)
            for k in sorted(ss):
                # print k
                # print '{0}: {1}, '.format(k, ss[k])
                polarity_score[k] += ss[k]
            
        # print polarity_score
        sum_values = sum(polarity_score.values())
        for k,v in polarity_score.iteritems():
            polarity_score[k] = 1.0*v/sum_values

        results[cand] = polarity_score
    # 'clinton': {'neg': 0.04331722016447989, 'neu': 0.7758717463642406, 'pos': 0.07601785314131007, 'compound': 0.1047931803299694}
    # 'trump': {'neg': 0.04811920673768291, 'neu': 0.8013294784528876, 'pos': 0.07236397646928304, 'compound': 0.07818733834014621}
    return results


def get_other_wikipedia_articles():
    """
    @return a dict of topics from several wikipedia articles to the text
    """
    topics = ['Dictator', 'Russia', 'China', 'North_Korea', 'Political_freedom', 'Cookie', 'Santa_Claus', 'Education', 'Technology']
    articles = {}

    for topic in topics:
        articles[topic] = wikipedia.page(topic).content.encode('utf-8')

    return articles


def wikipedia_document_distance():
    """
    Gets the pairwise document distance between 2 wikipedia articles
    """
    candidates = get_wikipedia_data()
    articles = get_other_wikipedia_articles()
    topics = candidates.keys() + articles.keys()
    documents = candidates.values() + articles.values()
    tfidf = TfidfVectorizer().fit_transform(documents)
    # no need to normalize, since Vectorizer will return normalized tf-idf
    pairwise_similarity = tfidf * tfidf.T

    distance = {}
    # print topics
    for i in xrange(len(candidates.keys())):
        distance[candidates.keys()[i]] = {}
        for j in xrange(2, len(topics)):
            distance[candidates.keys()[i]][topics[j]] = pairwise_similarity[(i,j)]

    # 'clinton': {'Santa_Claus': 0.59740676869753961, 'Political_freedom': 0.58216361267637096, 'North_Korea': 0.71676388689555781, 'China': 0.74716457057480512, 'Cookie': 0.41885077235168289, 'Dictator': 0.5815162187745383, 'Education': 0.70027094705960868, 'Technology': 0.70602510860154444, 'Russia': 0.75875347612359123
    # 'trump': {'Santa_Claus': 0.4872585234552006, 'Political_freedom': 0.45822297226088582, 'North_Korea': 0.56942490292159931, 'China': 0.59602212550185751, 'Cookie': 0.3371661857481143, 'Dictator': 0.46389224527696782, 'Education': 0.55642868808934209, 'Technology': 0.55439661564371012, 'Russia': 0.60152655815622524
    return distance
