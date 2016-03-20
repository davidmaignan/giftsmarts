import nltk
from nltk.book import *

class Nltk:

    def findConcordance(keywords, text):
        return text.common_contexts(keywords)
