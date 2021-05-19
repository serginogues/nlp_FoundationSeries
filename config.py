import os
import re
import json
import numpy as np
import logging
import pandas as pd
from tqdm import tqdm
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ngrams, PorterStemmer, WordNetLemmatizer
from collections import Counter
from itertools import combinations, permutations, islice, tee
import spacy
from spacy import displacy
from spacy.matcher import Matcher
import neuralcoref

logging.basicConfig(level=logging.CRITICAL)
print("Start CONFIG")

# region params
# PREPROCESS PARAMETERS:
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
lemmatizer = WordNetLemmatizer()
punctuation_tokens = {',', '.', '--', '-', '!', '?', ':', ';', '``', "''", '(', ')', '[', ']', '...'}

# NER PARAMETERS:
honorific_words = ['Dr.', 'Prof.', 'Mr.', 'Ms.', 'Msr.', 'Jr.', 'Sr.', 'Lord', 'Sir', 'Professor', 'Doctor', 'King',
                   'Commdor', 'Lady', 'Captain', 'Colonel', 'Miss', 'General', 'Mayor']
person_verbs_ = ['said', 'sniffed', 'met', 'greet', 'walked', 'respond', 'talk', 'think', 'hear', 'wait', 'pause',
                 'write', 'smile', 'answer', 'wonder', 'reply', 'read', 'sit', 'muttered', 'fumble', 'ask', 'sigh',
                 'frowned', 'cry', 'chuckled', 'murmured']
person_verbs = [lemmatizer.lemmatize(w, pos='v') for w in person_verbs_]
location_name = ['planet', 'kingdom', 'world', 'region', 'location', 'republic', 'street', 'neighborhood', 'realm', 'sight']
location_name_pattern = [{'POS': 'NOUN'}, {'LOWER': 'of'}, {'POS': 'PROPN'}]
travel_to_verbs_ = ['go', 'travel', 'move', 'exiled']
travel_to_verbs = [lemmatizer.lemmatize(w, pos='v') for w in travel_to_verbs_]
travel_to_pattern = [{'POS': 'VERB'}, {'LOWER': 'to'}, {'POS': 'PROPN'}]
be_in_pattern = [{'POS': 'AUX'}, {'LOWER': 'in'}, {'POS': 'PROPN'}]
be_on_pattern = [{'POS': 'AUX'}, {'LOWER': 'on'}, {'POS': 'PROPN'}]

# COREFERENCE RESOLUTION
neuralcoref.add_to_pipe(nlp)

# MAIN PARAMETERS:
with open("FoundationTrilogy.txt", "r", encoding="utf-8") as f:
    FoundationTrilogy = f.read()
