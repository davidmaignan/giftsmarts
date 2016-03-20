import nltk
from gensim.models import Word2Vec
from nltk.corpus import brown

brown_w2v = Word2Vec(brown.sents())

class Nltk:

    def find_concordance(keyword, text):
        tokens = nltk.word_tokenize(text)
        nltk_text = nltk.Text(tokens)
        return nltk_text.similar(keyword)

    def find_similar(keyword):
        return brown_w2v.most_similar(keyword, top=10)
