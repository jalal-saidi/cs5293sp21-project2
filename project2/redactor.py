import sklearn
import spacy
import glob
import io
import os
import pdb
import sys
import json

nlp = None

# This function redacts and extract features and labels for a person name from a given text and saves them to a dictionary
# The parameters for this functions are
# 1) The input text file
# 2) The result dictionary that features and lables are saved into
# 3) The file name that features belongs to
# The features types are:
# 1) The lenght of name
# 2) Whether the name has space
# 3) The gender of name
 
def redact(text,result_dict,file_name):
   
   # The gender arrays
   male=['he','his','him','himself']
   female=['she','her','her','herself']
   doc = nlp(text)
   redacted = []
   D = []
   for sent in doc.sents:
       gender_found=False
       for word in sent.ents:
           if word.label_== 'PERSON':
               d = {}
               d["length"] = len(word.text)
               d["spaces"] = 1 if " " in word.text else 0
               d["gender"]= 0
               if not gender_found:
                   for token in sent:
                      if  token.text.lower() in male  and (token.pos_== 'PRON'):
                         d["gender"]=1
                         gender_found=True
                         break
                      if  token.text.lower() in female  and (token.pos_== 'PRON'):
                         d["gender"]=2
                         gender_found=True
                         break
              
               redacted.append((word.start_char,len(word.text)))
               D.append((d,word.text,word.start_char,len(word.text)))
   if len(D)!=0:
       # Save the array of feature and labels to the a dictionary
       # The key is the file name 
       result_dict[file_name]=D
   return redacted

# This functions requires two inputs:
# 1) The directory where the inputs are stored
# 2) The output directory where the redacted files and the JSON file containing the features and labels are stored

def launcher(input,output):
   # The final result dictionary
   result_dict= {}
   # Opening all text files from the input directory
   for thefile in glob.glob(input+'/*.txt'):
       with io.open(thefile, 'r', encoding='utf-8') as fyl:
           file_name = thefile[thefile.rindex('/')+1:]+'.redacted'
          
           
           text = fyl.read()
           redacted=redact(text,result_dict,file_name)
           to_write=list(text)
           for location in redacted:
               for i in range(location[0],location[0]+location[1]):
                  to_write[i]= '\u2588'
           
           to_write=''.join(to_write)
           file_=open(output+'/'+file_name,"w")
           file_.write(to_write)
           file_.close() 
   # Save the result dictionary into a JSON file
   with open(output+"/result.json", "w") as outfile: 
    json.dump(result_dict, outfile)

# The main function requires two command line arguments
# 1) The input directory where the text files should be used for redaction and feature extraction
# 2) The output directory where the redacted file and JSON files containing features and labels are stored
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_lg")
    
    output = sys.argv[-1]
    input = sys.argv[-2]
    # Remove the old redacted files so it can be replaced by the new ones
    for f in glob.glob(output+'/'+'*.redacted'):
        os.remove(f)
    # Remove the old JSON file of features and labels  so it can be replaced by the new one
    if os.path.exists(output+"/result.json"):
        os.remove(output+"/result.json")
    launcher(input,output)

