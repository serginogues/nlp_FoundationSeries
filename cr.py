"""
Coreference resolution model
Unification of Character Occurrences (alias resolution): grouping proper nouns referring to the same character
"""
from config import predictor


def coreference_resolution(entity_list, text):
    predictor.coref_resolved(text)
    return entity_list[0]
