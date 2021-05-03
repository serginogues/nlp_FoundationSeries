# pip install -r requirements.txt
from foundationBooks import FoundationTrilogy, Target_people, Target_locations
import spacy
import numpy as np
from spacy.matcher import Matcher
from spacy import displacy
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ngrams, PorterStemmer, WordNetLemmatizer
import re
from collections import Counter
import neuralcoref
from tqdm import tqdm
from itertools import combinations, permutations
import pandas as pd
# import nltk
# nltk.download('wordnet', quiet=True)
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
neuralcoref.add_to_pipe(nlp)

"""
- Preprocessing
- Entity extraction with Rules Based + Snorkel
- Coreference and negation handling
- Validation
- Visualization
"""

"""
Related work
https://www.analyticsvidhya.com/blog/2020/06/nlp-project-information-extraction/
https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/?utm_source=blog&utm_medium=introduction-information-extraction-python-spacy
https://medium.com/agatha-codes/using-textual-analysis-to-quantify-a-cast-of-characters-4f3baecdb5c
https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
https://www.analyticsvidhya.com/blog/2020/07/part-of-speechpos-tagging-dependency-parsing-and-constituency-parsing-in-nlp/
https://cogsci.mindmodeling.org/2012/papers/0096/paper0096.pdf
https://github.com/isthatyoung/NLP-Characters-Relationships/blob/master/code/Preprocessing.py
https://github.com/emdaniels/character-extraction/blob/master/README.md
https://github.com/susanli2016/NLP-with-Python/blob/master/NER_NLTK_Spacy.ipynb

"""

"""
Dependency grammar

Dependency grammar example:
TOM <-nsubj- CANCELED (root) --------dobj------------> FLIGHTS --nmod-> HOUSTON 
                                [THE MORNING]                    [TO]
- CANCELED is the predicate (root)
- TOM is the subject (nsubj)
- FLIGHTS is the direct object (dobj)

Clausal Argument relations:
    - NSUBJ - nominal subject
    - DOBJ - direct object
    - IOBJ - indirect object
    - CCOMP - clausal complement
    - XCOMP - open clausal complement

Nominal Modifier relations:
    - NMOD - nominal modifier
    - AMOD - adjective modifier
    - NUMMOD - numeric modifier
    - APPOS - positional modifier
    - DET - Determiner
    - CASE prep, etz
    
Hint: Who-Who? Find speaker and subject of sentences
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_)

>> looking look VERB VBG ROOT
"""

"""
Report in research paper format
Sections:
    - Abstract - done
    - Introduction - done
    - Background (related work) - done
    - Approach - done
    - Dataset (book + Validation points) - done
    - Algorithms
    - Results
    - Future research
    - References
Add as well in the report what doubts we have and what is not clear
"""
