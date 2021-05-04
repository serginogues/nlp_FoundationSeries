import json
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

with open("FoundationTrilogy.txt", "r", encoding="utf-8") as f:
    FoundationTrilogy = f.read()
