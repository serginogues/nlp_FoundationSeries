from config import *


def all_mentions(doc):
    """All the "mentions" in the given text:"""
    for cluster in doc._.coref_clusters:
        return cluster.mentions


def pronoun_references(doc):
    """Pronouns and their references:"""
    list = []
    for token in doc:
        if token.pos_ == 'PRON' and token._.in_coref:
            for cluster in token._.coref_clusters:
                list.append((token.text, cluster.main.text))
    return list

"""if __name__ == "__main__":
    doc = nlp(test)
    dependency_graph(doc)
    if doc._.has_coref:
        print(all_mentions(doc))
        print(pronoun_references(doc))"""
