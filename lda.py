import os
from nltk.tokenize import RegexpTokenizer
# from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
# en_stop = get_stop_words('en')
with open('stop_words.txt') as f:
    stop_words = set(f.read().split())

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

person = 'obama'

filenames = map(lambda x: '%s/' % person + x, filter(lambda x: x != '.DS_Store', os.listdir(person)))

doc_set = []

for filename in filenames:
    with open(filename) as f:
        doc_set.append(f.read().decode('utf-8'))

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
lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=4, id2word = dictionary, passes=20)

lda_model.save('%s_model' % person)
