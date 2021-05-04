"""
Coreference resolution
https://neurosys.com/article/intro-to-coreference-resolution-in-nlp/
Unification of Character Occurrences (alias resolution): grouping proper nouns referring to the same character

Sherlock Holmes can also be called “Mr. Holmes” or “Sherlock”.
“Mr. Holmes” can refer to both Sherlock Holmes and his brother Mycroft Holmes.
"""
from utils import *


def all_mentions(doc):
    """All the "mentions" in the given text:"""
    if doc._.has_coref:
        for cluster in doc._.coref_clusters:
            return cluster.mentions
    else:
        return None


def pronoun_references(doc):
    """Pronouns and their references:"""
    list = []
    for token in doc:
        # if token.pos_ == 'PRON' and token._.in_coref:
        for cluster in token._.coref_clusters:
            list.append((token.text, cluster.main.text))
    return list


def similar_names(alias, name):
    if alias in name or name in alias:
        return True
    else:
        return False


def is_name(alias, name, parsed=False):
    """
    len(alias) == 2 and len(
    Example:
        Name = Bayta
        alias = Bayta Darell
        return True because Name is the name of alias
    Example:
        Name = Darell
        alias = Bayta Darell
        return False because Name is the surname of alias
    """
    if parsed:
        for i, word in enumerate(alias):
            if i == 0 and str(word) == name:
                return True
        return False
    else:
        for i, word in enumerate(alias.split(" ")):
            if len(alias.split(" ")) > 1 and i == 0 and str(word) == name:
                return True
        return False


def get_all_alias(entity_list, parsed_list):
    names_list = []
    for name in entity_list:
        alias_list = []
        for doc in parsed_list:
            for ent in doc.ents:
                if str(ent) != name and similar_names(str(ent), name):
                    if len(ent) == 2 and "'" not in str(ent):
                        alias_list.append(str(ent))

        alias_list = Counter(alias_list).most_common(6)
        alias_list = [x[0] for x in alias_list if int(x[1]) > 1]
        alias_list.insert(0, name)
        names_list.append(alias_list)

    print("Found all alias")
    return names_list


def compare_entities(entity_list):
    # if two entities share an alias
    for a, b in combinations(entity_list, 2):
        share = [i for i in a if i in b]
        if len(share) > 0:
            if not is_name(share[0], a[0]):
                a.remove(str(share[0]))
            elif not is_name(share[0], b[0]):
                b.remove(str(share[0]))
    print("Name and surname alias resolution finished")


def alias_resolution(entity_list, parsed_list):
    names_list = get_all_alias(entity_list, parsed_list)
    compare_entities([x for x in names_list if len(x) > 1])

    final_list = []
    for entity in names_list:
        if len(entity) == 1:
            final_list.append([entity[0]])
        elif len(entity) == 2:
            final_list.append([entity[0], entity[1]])
        else:
            # resolve "Foundation" alias
            if "Foundation" in entity:
                final_list.append([entity[0], entity[3]])
                final_list.append([entity[1]])
                final_list.append([entity[2]])
            else:
                final_list.append([entity[0], entity[1]])
                for i, name in enumerate(entity):
                    if i != 0 and i != 1:
                        final_list.append([name])

    return final_list


def coreference_resolution(entity_list, span):
    return entity_list[0]
