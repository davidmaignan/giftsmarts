import nltk
from gensim.models import Word2Vec
from nltk.corpus import brown
from app.constants import AMAZON_CATEGORIES
from nltk.tag import pos_tag
from app.config.config import amazon


brown_w2v = Word2Vec(brown.sents())

amazon_keywords = [AMAZON_CATEGORIES[0]]

class Nltk:

    def find_concordance(keyword, text):
        tokens = nltk.word_tokenize(text)
        nltk_text = nltk.Text(tokens)
        return nltk_text.similar(keyword)

    def find_similar(keyword):
        return brown_w2v.most_similar(keyword, top=10)

    def generate_searches(posts):
        results = {}
        nouns = []
        for p in posts:
            tagged_sent = pos_tag(p.story.split())
            propernouns = []
            last_noun = False
            for word,pos in tagged_sent:
                if pos == 'NNP':
                    if last_noun:
                        propernouns[-1] = propernouns[-1] + ' ' + word
                    else:
                        propernouns.append(word)
                        last_noun = True
                else:
                    last_noun = False

            for n in propernouns:
                if n == "I’m" or n == "It’s" or n == "Can’t":
                    continue
                results[n.replace('.', '')] = True

        for r in results.keys():
            nouns.append(r)

        return nouns
