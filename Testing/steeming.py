from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps=PorterStemmer()


def steemer(words):
    newwords=[]
    for w in words:
        newwords.append(ps.stem(w))
    return newwords



        
