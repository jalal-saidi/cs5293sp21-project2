
import sklearn
import spacy
import glob
import io
import os
import pdb
import sys


from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

nlp = None

def make_features(text, ne="PERSON"):
    doc = nlp(text)
    D = []
    for sent in doc.sents:
        for e in sent.ents:
            if e.label_ == ne:
                d = {}
                # d["name"] = e.text # We want to predict this
                d["length"] = len(e.text)
                d["word_idx"] = e.start
                d["char_idx"] = e.start_char
                d["spaces"] = 1 if " " in e.text else 0
                # gender?
                # Number of occurences?
                D.append((d, e.text))
    return D


def main(glob_text):
    features = []
    for thefile in glob.glob(glob_text):
        with io.open(thefile, 'r', encoding='utf-8') as fyl:
            text = fyl.read()
            features.extend(make_features(text))


    v = DictVectorizer(sparse=False)  

   
    clf = DecisionTreeClassifier()
    clf1 = RandomForestClassifier()
    clf2 = KNeighborsClassifier(n_neighbors=3)

    print("Cross Val Score Decision Tree", cross_val_score(clf,
                                               v.fit_transform([x for (x,y) in features]),
                                               [y for (x,y) in features],
                                               cv=5))
    print("Cross Val Score Random Forest: ", cross_val_score(clf1,
                                               v.fit_transform([x for (x,y) in features]),
                                               [y for (x,y) in features],
                                               cv=5))
    print("Cross Val Score for KNeighbors : ", cross_val_score(clf2,
                                               v.fit_transform([x for (x,y) in features]),
                                               [y for (x,y) in features],
                                               cv=5))

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_lg")
    main(sys.argv[-1])
