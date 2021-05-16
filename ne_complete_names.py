"""
First, entities are found in ner.py
In this section the complete name of every person NE (found during ner.py) is found
#TODO: do inference and alias resolution during this step?
"""
from config import Counter, combinations, FULL_NAMES, honorific_words, tqdm


def similar_names(alias, name):
    """
    Returns true if one word contains the other or viceversa
    """
    if alias in name or name in alias:
        return True
    else:
        return False


def get_all_alias(entity_list, parsed_list):
    """
    Gets name and surname of NE
    """
    print("Start GET_FULL_NAMES")
    names_list = []
    for nn in tqdm(range(len(entity_list))):
        name = entity_list[nn]
        alias_list = []
        for doc in parsed_list:
            for i, token in enumerate(doc):
                if i < len(doc)-1 and token.pos_ == "PROPN" and doc[i+1].pos_ == "PROPN":
                    ent = str(token) + " " + str(doc[i+1])
                    if ent != name and similar_names(ent, name):
                        alias_list.append(ent)

        alias_list = Counter(alias_list).most_common(6)
        alias_list = [x[0] for x in alias_list if int(x[1]) > 1]
        for alias in alias_list:
            if any([w for w in honorific_words if w in alias.split(" ")[0]]):
                alias_list.remove(alias)

        alias_list.insert(0, name)
        names_list.append(alias_list)

    return names_list


def is_name(alias, name, parsed=False):
    """
    len(alias) == 2 and len(
    Case 1:
        Name = Bayta
        alias = Bayta Darell
        return True because Name is the name of alias
    Case 2:
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


def compare_entities(entity_list):
    """
    If two entities share an alias
    """
    for a, b in combinations(entity_list, 2):
        share = [i for i in a if i in b]  # a list of entities sharing the same name or surname
        if len(share) > 0:
            if not is_name(share[0], a[0]):
                a.remove(str(share[0]))
            elif not is_name(share[0], b[0]):
                b.remove(str(share[0]))


def get_full_named_entities(entity_list, parsed_list):
    """
    Once entities are found by ,
    :param entity_list: list of found entities belonging to 'person' category
    :param parsed_list: list of parsed sentences from Spacy
    """
    if FULL_NAMES:
        names_list = get_all_alias(entity_list, parsed_list)
        compare_entities([x for x in names_list if len(x) > 1])

        final_list = []
        for entity in names_list:
            if len(entity) == 1:
                final_list.append([entity[0]])
            elif len(entity) == 2:
                final_list.append([entity[1]])  # only full name is considered, since it includes the abbreviation
            else:
                for i, name in enumerate(entity):
                    if i != 0:
                        final_list.append([name])
    else:
        final_list = [['Arkady Darell'], ['Hari Seldon'], ['Raven Seldon'], ['Fiari Seldon'], ['Seldon Hardin'],
                      ['Ducem Barr'], ['Onum Barr'], ['Bayta Darell'], ['Hober Mallow'], ['Fie'], ['Gaal Dornick'],
                      ['Salvor Hardin'], ['Toran Darell'], ['Pelleas Anthor'], ['Stettin'], ['Ebling Mis'], ['Dorwin'],
                      ['Homir Munn'], ['Flomir Munn'], ['Bail Channis'], ['Han Pritcher'], ['Flan Pritcher'],
                      ['Arcadia Darell'], ['Brodrig'], ['The Mule'], ['Speaker'], ['Lewis Pirenne'], ['Pappa'],
                      ['Jorane Sutt'], ['Randu'], ['Indbur'], ['Jole Turbor'], ['Magnifico Giganticus'], ['Verisof'],
                      ['Wienis'], ['Commdor Asper'], ['Ankor Jael'], ['Sef Sermak'], ['Lepold'], ['Sennett Forell'],
                      ['Mayor Hardin'], ['dryly'], ['Kleise'], ['Mamma'], ['Linge Chen'], ['Jord Fara'], ['Yohan Lee'],
                      ['Lee Senter'], ['Lewis Bort'], ['Master'], ['Pherl'], ['Fran'], ['Elvett Semic'], ['Walto'],
                      ['Theo Aporat'], ['Eskel Gorov'], ['Fox'], ['Elders'], ['Preem Palver'], ['Avakim'], ['Advocate'],
                      ['Lameth'], ['Fulham'], ['Galactic Empire'], ['Second Empire'], ['Les Gorm'], ['Limmar Ponyets'],
                      ['Emperor'], ['Bel Riose'], ['Second Foundation'], ['Second Foundationer'], ['First Foundation'],
                      ['Lathan Devers'], ['Dad'], ['Capsule'], ['Iwo'], ['Ovall Gri'], ['Hella'], ['Jord Commason'],
                      ['Plan'], ['Student'], ['Lev Meirus'], ['Poochie']]

    print("NER finished. Found:", len(final_list), "characters.")
    return final_list
