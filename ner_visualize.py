from preprocess import get_texts
from config import spacy, FoundationTrilogy, displacy
from utils import read_list
from spacy.tokens import Span
from validation import list_of_values

text = "When Hardin denied owning the Journal"

sentences = [(i,x) for i,x in enumerate(get_texts(FoundationTrilogy)) if text in x][0]
index = sentences[0]
sentence = sentences[1]
predicted = [y for idx,y in enumerate(read_list('predicted')) if idx==index][0]
print(sentence)
nlp = spacy.load("en_core_web_sm", disable=['ner'])
doc = nlp(sentence)
tags = list_of_values(predicted, doc)

dict_list = []
KEYS = ['start_idx', 'end_idx', 'text', 'type']
[dict_list.append(dict(zip(KEYS, elem))) for elem in tags]

"""spans = []
for sp in tags:
    spans.append(Span(doc, int(sp[0]), int(sp[1]), label=sp[2]))"""

spans = []
for sp in dict_list:
    spans.append(Span(doc, int(sp['start_idx']), int(sp['end_idx']), label=sp['type']))

doc.ents = spans
colors = {"PER": "linear-gradient(90deg, #aa9cfc, #fc9ce7)", "LOC": "linear-gradient(90deg, #aa9cfc, #fc9ce7)"}
options = {"ents": ["PER", "LOC"], "colors": colors}
displacy.serve(doc, style="ent", options=options)
# go to http://localhost:5000/




