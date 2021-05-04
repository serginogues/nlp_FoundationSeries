import re
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ngrams, PorterStemmer, WordNetLemmatizer
from collections import Counter
from itertools import combinations, permutations

import spacy
from spacy import displacy
from spacy.matcher import Matcher
import neuralcoref

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
neuralcoref.add_to_pipe(nlp)

# import nltk
# nltk.download('wordnet', quiet=True)

with open("FoundationTrilogy.txt", "r", encoding="utf-8") as f:
    FoundationTrilogy = f.read()
