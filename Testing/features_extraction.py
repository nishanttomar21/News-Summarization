import os
from Input import *
from preprocessing import *
from steeming import steemer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pickle
import numpy as np
import time
from Labeling import Label
import itertools
from generating import generate_summary
import csv
from readability import ParserClient
import requests
import json
import re
from nltk import sent_tokenize
from insertion import *


URL="https://newsapi.org/v1/articles?source=the-hindu&sortBy=latest&apiKey=3eef9af06d964786bbf2fc8a1c049668"
parser_client = ParserClient(token='7c8daeedd7726bf0c7d6b042098ee320ae336d87')

title_list=list()
title=""
image=list()
url=list()
author=list()
source=""
doc=""

def sentence_splitter(text):
    str_list=list(text)
    list1=re.finditer("[+-]?\d+\.\d+",text)
    list2=[]

    for each_elem in list1:
        list2.append(each_elem.span())


    for each_elem in list2:
        for i in range(each_elem[0],each_elem[1],1):
            if str_list[i]==".":
                str_list[i]='XYZ'

    text=''.join(str_list)    
    text=text.replace('.','. ')
    text=text.replace('XYZ','.')
    return text

def summly():
    sentencearray=[]
    sent_tfidf=[]
    sent_title=[]
    sent_position=[]
    sent_len=[]
    test_data=[]

    sentences=sent_tokenize(doc)

    for each_sent in sentences:
        each_sent=removePunctations(each_sent.lower())
        sent_words=word_tokenize(each_sent)
        sent_words=removeStopWords(sent_words)
        sent_words=steemer(sent_words)
        sentence=' '.join(sent_words)
        sentencearray.append(sentence)


 #   tf_pickle=open("tf.pickle","rb")
#    vect=pickle.load(tf_pickle)

    vect = CountVectorizer()
    vect.fit(sentencearray)

    test_dtm=vect.transform(sentencearray)

#    tfidf_pickle=open("tfidf.pickle","rb")          
#    tfidf=pickle.load(tfidf_pickle)

    tfidf=TfidfTransformer()
    tfidf.fit(test_dtm)

    tf_idf_matrix=tfidf.transform(test_dtm)

    TF=tf_idf_matrix.astype(np.float32) 

    Tf_Idf=TF.toarray()


    for index,each_TfIdf in enumerate(Tf_Idf):
        l=len(word_tokenize(sentencearray[index]))
        summ=0
        if l!=0:
            for i in each_TfIdf:
                summ+=i
            summ=summ/l

        sent_tfidf.append(summ)


    Title=removePunctations(title)
    titleWords=word_tokenize(Title)
    titleWords=removeStopWords(titleWords)
    titleWords=steemer(titleWords)
    

    for each_sent in sentencearray:
        sentenceWords=word_tokenize(each_sent)
        sent_title.append(TitleScore(titleWords,sentenceWords))


    length=len(sentencearray)
    for index,each_sent in enumerate(sentencearray):
        sent_position.append(SentencePositionScore(index+1,length))


    max_l=[]
    for each_sent in sentencearray:
        max_l.append(len(word_tokenize(each_sent)))
        
    max_length=max(max_l)


    for i in range(len(sentencearray)):
        sent_len.append(SentenceLengthScore(sentencearray[i],max_length))



    for i,j,k,l in zip(sent_tfidf,sent_title,sent_position,sent_len):
        test_data.append([i,j,k,l])


    classifier_pickle=open("clf.pickle","rb")
    clf=pickle.load(classifier_pickle)

    prediction=clf.predict(test_data)

    return generate_summary(prediction,doc)


def crawl_data():
    global title
    global doc
    global title_list
    
    file =  requests.get(URL)
    jsonObject = file.json()
    source=jsonObject['source']
    ja = jsonObject['articles']

    for a in ja:
        title_list.append(a['title'])
        image.append(a['urlToImage'])
        url.append(a['url'])
        author.append(a['author'])

    title_list = [item.lower() for item in title_list]

    clear_values()

    for i in range(len(ja)):
        parser_response = parser_client.get_article(url[i])
        article = parser_response.json()
        doc = article['content']
        
        doc = re.sub("<[^>]*>","",doc)
        doc = re.sub('&.*?;', '', doc)
        doc = re.sub('["]', '', doc)
        doc = re.sub('.*[^more-in]*more-in','',doc)
        doc = re.sub('\([^)]*\)','',doc)
        doc = re.sub('\[[^]]*\]','',doc)
        doc = re.sub('(?:Please Wait while comments are loading...)','',doc)
        doc = re.sub('on Monday|on Tuesday|on Wednesday|on Thursday|on Friday|on Saturday|on Sunday','',doc)
        doc = re.sub('\n','',doc)
        doc = re.sub('PTI','',doc)
        doc = re.sub('\.{3}',', ',doc)
        doc = re.sub('Rs.','Rs',doc)
        doc = re.sub('More In.*','',doc)
        doc = re.sub('(?:| Photo Credit:)','',doc)
        doc = re.sub('(?:Mr.)','Mr',doc)
        doc = re.sub('(?:Mrs.)','Mrs',doc)
        doc = re.sub('(?:Ds.)','Dr',doc)
        doc = re.sub('(?:Photo Credit:)','',doc)
        doc = re.sub('\| ','',doc)
        doc = sentence_splitter(doc)

        title = title_list[i]
        summary = summly()
        
        if(summary.count('.') <= 4):
           summary = Summary(doc,title)
           
        print("Summary: ",summary)
        print("Doc lenght -> ",len(sent_tokenize(doc)))
        print("Summary length -> ",len(sent_tokenize(summary)))
        insertion(title,image[i],url[i],summary,source,author[i])

 
crawl_data()
