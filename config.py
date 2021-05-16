import os
import re
import json
import numpy as np
import logging
logging.basicConfig(level=logging.CRITICAL)
import pandas as pd
from tqdm import tqdm
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ngrams, PorterStemmer, WordNetLemmatizer
from collections import Counter
from itertools import combinations, permutations, islice
import spacy
from spacy import displacy
from spacy.matcher import Matcher

from allennlp_models.pretrained import load_predictor
print("Start CONFIG")

# PREPROCESS PARAMETERS:
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
lemmatizer = WordNetLemmatizer()
# import nltk
# nltk.download('wordnet', quiet=True)
punctuation_tokens = {',', '.', '--', '-', '!', '?', ':', ';', '``', "''", '(', ')', '[', ']', '...'}


# NER PARAMETERS:
honorific_words = ['Dr.', 'Prof.', 'Mr.', 'Ms.', 'Msr.', 'Jr.', 'Sr.', 'Lord', 'Sir', 'Professor', 'Doctor', 'King', 'Commdor', 'Lady']
person_verbs_ = ['said', 'sniffed',  'met', 'greet', 'walked', 'respond', 'talk', 'think', 'hear', 'go', 'wait', 'pause', 'write', 'smile', 'answer', 'wonder', 'reply', 'read', 'sit', 'muttered', 'fumble', 'ask', 'sigh']
person_verbs = [lemmatizer.lemmatize(w, pos='v') for w in person_verbs_]
location_name = ['planet', 'kingdom', 'world', 'region', 'location', 'republic', 'street', 'neighborhood', 'realm']
location_name_pattern = [{'POS': 'NOUN'}, {'LOWER': 'of'}, {'POS': 'PROPN'}]
travel_to_verbs_ = ['go', 'travel', 'move', 'exiled']
travel_to_verbs = [lemmatizer.lemmatize(w, pos='v') for w in travel_to_verbs_]
travel_to_pattern = [{'POS': 'VERB'}, {'LOWER': 'to'}, {'POS': 'PROPN'}]
be_in_pattern = [{'POS': 'AUX'}, {'LOWER': 'in'}, {'POS': 'PROPN'}]
be_on_pattern = [{'POS': 'AUX'}, {'LOWER': 'on'}, {'POS': 'PROPN'}]


# COREFERENCE RESOLUTION
logging.getLogger('allennlp.common.params').disabled = True
logging.getLogger('allennlp.nn.initializers').disabled = True
logging.getLogger('allennlp.modules.token_embedders.embedding').setLevel(logging.CRITICAL)
logging.getLogger('urllib3.connectionpool').disabled = True
predictor = load_predictor("coref-spanbert")


# MAIN PARAMETERS:
with open("FoundationTrilogy.txt", "r", encoding="utf-8") as f:
    FoundationTrilogy = f.read()

STAGE = 2

PREPROCESS = True
NER = True
FULL_NAMES = True
LINKS = True
VISUALIZE = True
if STAGE == 2:
    # at Full names
    NER = False

elif STAGE == 3:
    # at CR + Alias Resolution
    PREPROCESS, NER, FULL_NAMES = False, False, False


