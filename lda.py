# from __future__ import division  # Python 2 users only
# import nltk, re, pprint
# from nltk import word_tokenize

# import os

# import textmining
# import lda

# def term_document_from_file(filenames, csv_filename='matrix'):
#     # Initialize class to create term-document matrix
#     tdm = textmining.TermDocumentMatrix()

#     # add the documents to the matrix
#     for filename in filenames:
#         with open(filename) as f:
#             doc = f.read()
#             # Add the document
#             tdm.add_doc(doc)

#     # Write out the matrix to a csv file. Note that setting cutoff=1 means
#     # that words which appear in 1 or more documents will be included in
#     # the output (i.e. every word will appear in the output). The default
#     # for cutoff is 2, since we usually aren't interested in words which
#     # appear in a single document. For this example we want to see all
#     # words however, hence cutoff=1.
#     tdm.write_csv('%s.csv' % csv_filename, cutoff=1)
#     # Instead of writing out the matrix you can also access its rows directly.
#     # Let's print them to the screen.
#     for row in tdm.rows(cutoff=1):
#             print row
import os
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

filenames = map(lambda x: 'obama/' + x, filter(lambda x: x != '.DS_Store', os.listdir('obama')))

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
    stopped_tokens = [i for i in tokens if not i in en_stop]
    
    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    
    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word = dictionary, passes=20)

# lda_model.save('obamamodel')

topics = lda_model.print_topics(-1)

for topic in topics:
    print topic

























