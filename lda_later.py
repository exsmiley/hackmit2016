import gensim
import requests

lda_model = gensim.models.ldamodel.LdaModel.load("obama_model")

topics = lda_model.show_topics()

queries = []

for topic in topics:
    words = map(lambda x: x[6:], topic[1].split(' + ')) + ['xkcd']
    queries.append(' '.join(words))

# url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query