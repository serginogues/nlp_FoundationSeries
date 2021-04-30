from foundationBooks import FoundationTrilogy, Target_people, Target_locations
import spacy
import numpy as np
from spacy.matcher import Matcher
from spacy import displacy
from nltk.tokenize import PunktSentenceTokenizer, TreebankWordTokenizer, RegexpTokenizer, sent_tokenize
from nltk import ngrams, PorterStemmer, WordNetLemmatizer
import re
from collections import Counter
import neuralcoref
# import nltk
# nltk.download('wordnet', quiet=True)
from tqdm import tqdm
import pandas as pd
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
neuralcoref.add_to_pipe(nlp)
# pip install -r requirements.txt

"""
- Preprocessing
- Entity extraction with Ruled Based + Snorkel
- Coreference and negation handling
- Validation
- Visualization
https://arxiv.org/pdf/1907.02704.pdf
1) The identification of characters. We distinguish two substeps:
    - Detect occurrences of characters in the narrative
        -  a character can appear under three forms in text: proper noun, nominal, and pronoun.
    - Unify these occurrences, i.e. to determine which ones correspond to the same character.
    In a text, the same character can appear under different names.
    The output of this step takes the form of a chronological sequence of unified character occurrences.

2) Detecting interactions between characters.
    - take into account conversations, and to consider that two characters interact when one talks to the other.
    With certain forms of narrative such as plays, in which speakers are given, this task is relatively straightforward.
    - situations where one character talks about the other.
    - all sorts of actions one character can perform on the other (besides conversing).
    - explicit or inferred social relationships such as being married, being relatives, or working together
    The output of the second step is a chronological sequence of interactions between characters.

3) The extraction of the proper graph
    - preprocess: simplifying the sequence of interactions by filtering and/or merging some of the characters under certain conditions.
    For example, when considering co-occurrences, some authors merge characters that always appear together
    - temporal integration, i.e. the aggregation of the previously identified interactions.
        - full integration and therefore leading to a static network, and those performing only
        a partial integration, and producing a dynamic network.
"""

"""
Related work
https://www.analyticsvidhya.com/blog/2020/06/nlp-project-information-extraction/
https://www.analyticsvidhya.com/blog/2020/06/nlp-project-information-extraction/?utm_source=blog&utm_medium=POS_DependencyParsing_ConstituencyParsing
https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/?utm_source=blog&utm_medium=introduction-information-extraction-python-spacy
https://medium.com/agatha-codes/using-textual-analysis-to-quantify-a-cast-of-characters-4f3baecdb5c
https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
https://www.analyticsvidhya.com/blog/2020/07/part-of-speechpos-tagging-dependency-parsing-and-constituency-parsing-in-nlp/
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
