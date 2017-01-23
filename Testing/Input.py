import os
import re

source=[]

def remove_agency_headers(doc):
    After_doc = re.sub('[0-9]+_[0-9]+',"",doc)
    After_doc = re.sub('[0-9]+\.[0-9]+',"",After_doc)
    After_doc = re.sub('[A-Z][A-Za-z, ]+ [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} UTC',"",After_doc)
    After_doc = re.sub('[0-9]{2}:[0-9]{2}:[0-9]{2} UTC',"",After_doc)
    After_doc = re.sub('\-\-(January|February|March|April|May|June|July|August|September|October|November|December) [0-9]{2}[, ]*[0-9]{4}:?',"",After_doc)
    After_doc = re.sub('Cox News Service SAN FRANCISCO -',"",After_doc)
    After_doc = re.sub('^[A-Za-z0-9\., ]+ \(Xinhua\)',"",After_doc)
    return After_doc


def remove_reported_said(doc):

    After_doc = re.sub('[,|('')|"] [^,]+ (announced|reported|told|said|say|revealed)+( ?[^\.]+)*',"",doc)
    After_doc = re.sub('^[a-z]+ (said) (that )?',"",After_doc)
    return After_doc


def according_to(doc):
    return re.sub(', ?according to .+\.',".",doc)


def remove_transcation(doc):
    return re.sub('([Nn]onetheless|[Mm]oreover),? ?',"",doc)


def redundant_intros(doc):
    After_doc = re.sub('^The study (shows|reveals) that the ',"",doc)
    After_doc=  re.sub('^According to [^,]+, ?',"",After_doc)
    return After_doc

# Eg. joe is, 35, ...
def age(doc):
    return re.sub(', ?[0-9]+, ?'," ",doc)

def days_of_week(doc):
    After_doc = re.sub('(([Oo]n|[Aa]s of) )?(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)[ \.,]',"",doc)
    After_doc = re.sub('(([Oo]n|[Aa]s of) )?(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ',"",After_doc)
    return After_doc


def remove_gmt(doc):
    doc = re.sub('\([0-9]+ GMT\)',"",doc)
    return doc

def caps_opening(doc):
    After_doc = re.sub('^[A-Z]{2,},? ',"",doc)
    return After_doc
