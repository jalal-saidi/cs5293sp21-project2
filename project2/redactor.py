import sklearn
import spacy
import glob
import io
import os
import pdb
import sys
import json

nlp = None

def redact(text,result_dict,file_name):
   doc = nlp(text)
   redacted = []
   D = []
   for sent in doc.sents:
       for word in sent.ents:
           if word.label_== 'PERSON':
               d = {}
               d["length"] = len(word.text)
               d["spaces"] = 1 if " " in word.text else 0
               redacted.append((word.start_char,len(word.text)))
               D.append((d,word.text,word.start_char,len(word.text)))
   if len(D)!=0:
       result_dict[file_name]=D
   return redacted

def launcher(input,output):
   result_dict= {}
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
   with open(output+"/result.json", "w") as outfile: 
    json.dump(result_dict, outfile)
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_lg")
    output = sys.argv[-1]
    input = sys.argv[-2]
    for f in glob.glob(output+'/'+'*.redacted'):
        os.remove(f)
    launcher(input,output)

