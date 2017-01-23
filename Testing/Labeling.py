from __future__ import division
import re
from nltk.tokenize import sent_tokenize
from preprocessing import *
from steeming import steemer


text="Nishant how are you. Satyam how are you. He always want to live a happy life. shivam is a good boy"
keyphrases="shivam is a good. He always want happy life. nishant   you."

def split_into_sents(text):
    text=text.replace("\n",".")
    return text.split(".")

def  split_into_paragraphs(text):
    return text.split("\n\n")

def sent_inter(sent1,sent2):
    s1=set(sent1.split(" "))
    s2=set(sent2.split(" "))
    if (len(s1)+ len(s2))==0:
        return 0

    
    return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)


def format_sentence(sentence):
    sentence = re.sub(r'\W+', '', sentence)
    return sentence

def get_Labeled_sent(keyphrase,text):

    sentences = sent_tokenize(text)   ##Remark1

    for index,each_sent in enumerate(sentences):
        each_sent=removePunctations(each_sent.lower())
        sent_words=word_tokenize(each_sent)
        sent_words=removeStopWords(sent_words)
        sent_words=steemer(sent_words)
    
        sentences[index]=' '.join(sent_words)

    n=len(sentences)
    array1=[]
    array2=[]

    keyphrase=removePunctations(keyphrase.lower())
    keyphrase_words=word_tokenize(keyphrase)
    keyphrase_words=removeStopWords(keyphrase_words)
    keyphrase_words=steemer(keyphrase_words)
    keyphrase=' '.join(keyphrase_words)
    
    for i in range(0,n):
        array1.append(sent_inter(keyphrase,sentences[i]))

    array2=sorted(array1, reverse=True)


    return array1.index(array2[0])

    

def get_Labsent_indexes(keyphrases,text):
    array=[]
    Total_keyphrases=sent_tokenize(keyphrases)
    for keyphrase in Total_keyphrases:
        array.append(get_Labeled_sent(keyphrase,text))

    return array
    

def Label(keyphrases,text):
    sentences = sent_tokenize(text)
    n=len(sentences)
##    print(n)
    array1=[]
    array2=[]
    array1=get_Labsent_indexes(keyphrases,text)
    for i in range(n):
        if i in array1:
            array2.append(1)
        else:
            array2.append(0)

    return array2
