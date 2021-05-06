
import sklearn
import spacy
import glob
import io
import os
import pdb
import sys
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import numpy


from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier


# This function unredacts the redacted files by
# 1) Spliting the data to train and test set
# 2) Train on the training set and create a Random forest Model
# 3) Predict on the test set and unredact their text and save the unredacted files in a new folder

# This function requires a parameter where the redacted data exists
def unredact(redact_dir):
    if os.path.exists(redact_dir+"/result.json"):
       with open(redact_dir+'/result.json') as f:
         data = json.load(f)
         all_files=list(data.keys())
         

         data_np = numpy.array(all_files)
         # Allocate 75% for training and 25% for testing
         train_keys,test_keys=train_test_split(data_np,test_size=0.25) 
         train_x=[]
         train_y=[]
         train_location=[]
         for k in train_keys:
             items= data[k]
             for item in items:
               train_x.append(item[0])
               train_y.append(item[1])
               train_location.append((k,item[2],item[3]))
         
         test_x=[]
         test_y=[]
         test_location=[]
         for k in test_keys:
             items= data[k]
             for item in items:
               test_x.append(item[0])
               test_y.append(item[1])
               test_location.append((k,item[2],item[3]))    
        
        
  
         # The dict vectorizer for transforming the features
         v = DictVectorizer(sparse=False)  
         train_x=v.fit_transform(train_x)
    
         # Create the random forest model
         random_forest = RandomForestClassifier()
         random_forest.fit(train_x,train_y)
         
         # Performing the prediction
         preds=random_forest.predict(v.fit_transform(test_x))
         # Printing  the result
         print(classification_report(test_y, preds))
         
         # Performing the unredaction process by reading the file names and location of text should be unredacted from the JSON file
         for index,pred in enumerate(preds):
             loc1= test_location[index]
             try:
                f2=open(redact_dir+"/"+"test-unredacted/"+loc1[0], "r")
                content=f2.read()
                content=list(content)
             
             except:
             
                f2 = open(redact_dir+"/"+loc1[0], "r")
                content=f2.read()
                content=list(content)
                f3=open(redact_dir+"/"+"test-original/"+loc1[0], "w")
                f3.write("".join(content))
                f3.close()
             f2.close()
             idx=0
             for letter in pred:
                content[loc1[1]+idx]=letter
                idx+=1

             f2=open(redact_dir+"/"+"test-unredacted/"+loc1[0], "w")
             f2.write("".join(content))


if __name__ == "__main__":
    redacted_dir =  sys.argv[-1]
    # Removing the old unredacted files
    for f in glob.glob(redacted_dir+'/test-unredacted/'+'*.redacted'):
        os.remove(f)
    for f in glob.glob(redacted_dir+'/test-original/'+'*.redacted'):
        os.remove(f)
    unredact(redacted_dir)
