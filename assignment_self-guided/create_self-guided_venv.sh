  
#!/usr/bin/env bash

#if in worker2, first set the working directory 
#cd cds-language/src

VENVNAME=keyword_sentiment_environment

python3 -m venv $VENVNAME
source $VENVNAME/bin/activate
pip install --upgrade pip

pip install ipython
pip install jupyter
python -m ipykernel install --user --name=$VENVNAME

test -f requirements.txt && pip install -r requirements.txt
python -m spacy download en_core_web_sm

# then run the script: (in worker2 , it wouldn't be in the "src" folder, because the requirements and scripts are in the same folder)
#python3 src/keyword_headline_sentiment.py 

#then deactivate the environment
deactivate
echo "build $VENVNAME"
