import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn import preprocessing,cross_validation,neighbors,svm



train = pd.read_csv('training.csv')

label_pickle=open("labels.pickle","rb")
labels=pickle.load(label_pickle)

X=train.loc[:]

y=labels

X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.2)

clf=svm.SVC(kernel='linear',C=1,class_weight={1:20})
clf.fit(X_train,y_train)

save_classifier=open("clf.pickle","wb")
pickle.dump(clf,save_classifier)
save_classifier.close()

accuracy=clf.score(X_test,y_test)
print(accuracy)
