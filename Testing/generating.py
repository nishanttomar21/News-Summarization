from nltk.tokenize import sent_tokenize

##text="My name is Shivam Sharma. I am Pursuing My b.tech from Jiit Noida. I am a good boy."
##summary="My name is Shivam Sharma. I am a good boy."
##Label_list=[1,0,1]

def generate_summary(Label_list,text): ## this is a list of catchphrase sentences
    sentences=sent_tokenize(text)
    summary=[]
    for index,label in enumerate(Label_list):
        if label==1:
            summary.append(sentences[index])

    return ' '.join(summary)

##print(generate_summary(Label_list,text))  ## This return a string

            
