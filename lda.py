import os
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim


def generate_model(person):
    """
    Generates the LDA model for the candidate specified. Looks
    at the the .txt files in the directory under the directory
    of the person's name. Saves the model to <person>_model.
    """
    filenames = map(lambda x: '%s/' % person + x, filter(lambda x: x != '.DS_Store', os.listdir(person)))

    doc_set = []

    for filename in filenames:
        with open(filename) as f:
            doc_set.append(f.read().decode('utf-8'))

    tokenizer = RegexpTokenizer(r'\w+')

    # create English stop words list
    # en_stop = get_stop_words('en')
    with open('stop_words.txt') as f:
        stop_words = set(f.read().split())

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    # list for tokenized documents in loop
    texts = []

    # loop through document list
    for i in doc_set:
        
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in stop_words]
        
        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        
        # add tokens to list
        texts.append(stemmed_tokens)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)
        
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]

    # generate LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=20, id2word = dictionary, passes=20)

    lda_model.save('%s_model' % person)


def topics_from_people(person):
    """
    Gets the LDA model's topics for the person
    """
    lda_model = gensim.models.ldamodel.LdaModel.load("%s_model" % person)

    topics = lda_model.show_topics(num_topics=20)

    queries = []

    for topic in topics:
        words = map(lambda x: x[6:], topic[1].split(' + ')) + ['xkcd']
        queries.append(' '.join(words))

    return queries


def main():
    people = ['hillary', 'trump']

    for person in people:
        print "Generating model for %s..." % person
        generate_model(person)

        print "Topics for %s..." % person
        topics = topics_from_people(person)

        for topic in topics:
            print topic

if __name__ == '__main__':
    # main()
    generate_model('trump')
    topics = topics_from_people('trump')
    for topic in topics:
        print topic
