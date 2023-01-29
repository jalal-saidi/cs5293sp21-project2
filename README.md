Said Jalal Saidi

How to run: project 2 consists of two important Python files: the first file is redactor.py. The redactor.py should be run using: 
Pipenv run python project2/redactor.Py 'project2/all-data/sample' 'project2/all-data/sample/redacted'. 
It requires two command line arguments: a) the location where original text files should be used for redaction. B) the location where the redacted files and extracted features should be saved.

The second python file is unredactor.py. It should be run using:
Pipenv run python project2/unredactor.py  'project2/all-data/sample/redacted'
It requires one command line argument, the location where unredacted files exist. 

Libraries, dependencies, and virtual environment: first, a virtual environment is created using pyenv, with a 3.8.6 python version. Second, project1 module is installed in this virtual environment. Third, required libraries to run are installed such as "Pipenv". Fourth, required libraries for the program functionalities are installed such as spacy, which is necessary for extracting name entities and part of speech tagging. Other libraries such as sklearn are used for preprocessing such as DictVectorizer and splitting to training and testing. Moreover, RandomForestClassifier from Sklearn is used to train the models. Finally, the classification report is used for the model evaluation.

Assumptions: the redactor.py uses the input text files as input. It uses spacy entity to locate the name entities and redact them. Also, it extracts the features as well as their labels and saves them in a separate JSON file. The extracted features are the length, gender, and whether they include space or not. This JSON file, later on, will be used by the unredactor.Py for both training and testing. Unredactor.Py imports the JSON file as a dictionary. The keys for the dictionary are the file names of the redacted files. The values for the dictionary are arrays of features encoded as a dictionary. Also, the value includes the location of the redacted item in the given file. After, the training using random forest, it predicts a value for each redacted item and unredacted them. The result will be saved in a separate directory.
