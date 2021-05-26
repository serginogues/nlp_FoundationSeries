# Text Mining The Foundation Trilogy

### Author: Sergi Nogues Farres

A Rule-Based NER model to extract all the key entities and their connections from the Isaac Asimov's first three Foundation books, collectively known as the [Foundation Trilogy](https://asimov.fandom.com/wiki/Foundation_trilogy).

## Interactive Renders Guide
### NER on sentence
Go to [ner_visualize.py](ner_visualize.py) <br>
NUM parameter is the sentence's index from the book to be processed <br>
Run and go to http://localhost:5000/

### Character Network
Run [network_graph.py](network_graph.py)

### Galaxy map
Run [interactive_map.py](interactive_map.py)

## Code Guide
Run [main.py](main.py) to do preprocess + NER + entity relations + normalization <br>
NER is done at [ner.py](ner.py)<br>
Entities are linked at [entity_connections.py](entity_connections.py) <br>
[config.py](config.py) stores all configuration parameters such as [SpaCy](https://spacy.io/) pretrained en_core_web_sm model or the [Foundation Trilogy books](https://asimov.fandom.com/wiki/Foundation_trilogy). <br>
Normalization is done at [normalization.py](normalization.py) <br>
Validation results can be obtained running [validation.py](validation.py). <br>
Intermediate results are stored at [data_outputs](data_outputs) repo as .txt files.

<!--FOUNDATION

1 The Psychohistorians

- locations: Synnax, Trantor, Terminus
- People: Gaal Dornick, Hari Seldon, Galactic Empire, Foundation

2 The Encyclopedists

- locations: Anacreon, Terminus
- people: Anselm Haut Rodric, Salvor Hardin,The Mayor, (Dr. Bor Alurin)

3 The Mayors

- locations: Terminus, Four Kingdoms (Anacreon, Smyrno, Konom and Daribow)
- people: Salvor Hardin, Prince Regent Wienis

4 The Traders

- locations: Askone, Terminus
- people: Limmar Ponyets, Eskel Gorov, The Grand Master, Pherl

5 The Merchant Princes

- locations: Republic of Korell, Terminus
- people: Hober Mallow, Commdor Asper Argo, Commdora Licia Argo, Viceroy, Jord Parma

FOUNDATION AND EMPIRE

- locations: Trantor
- people: Bel Riose, Ducem Barr, Onum Barr (father), Lathan Devers, Cleon II, Ammel Brodrig

The Mule

- locations: Trantor, Terminus, Great Library
- people: Indbur III, Mule, Magnifico Giganticus (Mule), Toran Darell, Bayta Darell, Ebling Mis, Second Foundation

SECOND FOUNDATION

Search by the Mule

- locations: Tazenda, Rossem
- people: Bayta Darell, the Mule, Second Foundation, Han Pritcher, Foundation, Bail Channis, The First Speaker

Search by the Foundation

- locations: Kalgan, Terminus, Trantor
- people: First Foundation, Second Foundation, Toran Darell, Pelleas Anthor, Homir Munn, Elvett Semic, Jole Turbor, Arcadia Darell (Arkady), Lord Stettin, Callia, Preem Palver

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
https://neurosys.com/article/most-popular-frameworks-for-coreference-resolution/
https://neurosys.com/article/intro-to-coreference-resolution-in-nlp/
https://lvngd.com/blog/coreference-resolution-python-spacy-neuralcoref/
https://towardsdatascience.com/how-to-make-an-effective-coreference-resolution-model-55875d2b5f19

https://arxiv.org/pdf/1907.02704.pdf
1) The identification of characters. We distinguish two substeps:
    - Detect occurrences of characters in the narrative
        -  a character can appear under three forms in text: proper noun, nominal, and pronoun.
    - Unify these occurrences, i.e. to determine which ones correspond to the same character.
    In a text, the same character can appear under different names.
    As mentioned before, characters occurrences appear under three forms in text: proper nouns, nominals, and pronouns.
    Unifying these occurrences can be considered as a specific version of the coreference resolution problem,
    which consists in identifying sequences of expressions, called coreference chains, that represent the same concept.
    - The output of this step takes the form of a chronological sequence of unified character occurrences.

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
        a partial integration, and producing a dynamic network.-->
