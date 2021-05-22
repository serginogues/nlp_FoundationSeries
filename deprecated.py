from config import *

entities = [['Arkady Darell'], ['Hari Seldon'], ['Seldon Plan'], ['Seldon Crisis'], ['Raven Seldon'],
                      ['Seldon Convention'], ['Ducem Barr'], ['Onum Barr'], ['Bayta Darell'], ['Hober Mallow'],
                      ['Trader Mallow'], ['Flober Mallow'], ['Extinguishing Field'], ['Field Bearings'],
                      ['Salvor Hardin'], ['Toran Darell'], ['Gaal Dornick'], ['Pelleas Anthor'], ['Stettin'],
                      ['Ebling Mis'], ['Miss Erlking'], ['Dorwin'], ['Bail Channis'], ['Homir Munn'], ['Flomir Munn'],
                      ['Captain Pritcher'], ['Han Pritcher'], ['Flan Pritcher'], ['Colonel Pritcher'],
                      ['General Pritcher'], ['Mule'], ['First Speaker'], ['Arcadia Darell'], ['Brodrig'], ['Pirenne'],
                      ['Jorane Sutt'], ['Tomaz Sutt'], ['Pappa'], ['Randu'], ['Magnifico Giganticus'], ['Indbur'],
                      ['Jole Turbor'], ['Poly Verisof'], ['Wienis'], ['Limmar Ponyets'], ['Ankor Jael'],
                      ['Sennett Forell'], ['Sef Sermak'], ['Lepold I'], ['Eskel Gorov'], ['Callia'], ['Mayor Indbur'],
                      ['Mayor Hardin'], ['Jord Fara'], ['Grand Master'], ['Master Trader'], ['Bel Riose'],
                      ['General Riose'], ['Fran'], ['Kleise'], ['Mamma'], ['Yohan Lee'], ['Lee Senter'], ['Lewis Bort'],
                      ['Pherl'], ['Linge Chen'], ['Walto'], ['Theo Aporat'], ['Fox'], ['Elders'], ['Student'],
                      ['Elvett Semic'], ['Avakim'], ['Advocate'], ['Lameth'], ['Yate Fulham'], ['Galactic Empire'],
                      ['Second Empire'], ['First Empire'], ['Orsy'], ['Second Foundation'], ['First Foundation'],
                      ['Second Foundationer'], ['Encyclopedia Foundation'], ['Second Foundationers'],
                      ['Foundation Number'], ['Personal Capsule'], ['Iwo'], ['Mangin'], ['Ovall Gri'], ['Hella'],
                      ['Jord Commason'], ['Plan'], ['Lev Meirus'], ['Poochie'], ['Preem Palver']]

text = """Bayta's first sight of Haven was entirely the contrary of spectacular. Her husband pointed it out 
- a dull star lost in the emptiness of the Galaxy's edge. It was past the last sparse clusters, to 
where straggling points of light gleamed lonely. And even among these it was poor and inconspicuous. 
Toran was quite aware that as the earliest prelude to married life, 
the Red Dwarf lacked impressiveness and his lips curled self-consciously. "I know, Bay - It isn't exactly a proper 
change, is it? I mean from the Foundation to this." "A horrible change, Toran. I should never have married you."""


def token_is_candidate(token):
    """
    :return: True if token is proper name or adjective
    """
    if token.pos_ == 'PROPN' or token.pos_ == 'ADJ' and str(token) not in honorific_words:
        return True
    else:
        return False


def print_results_and_sort(entity_list, connection_list):
    for i, name in enumerate(entity_list):
        conn = [x for x in connection_list if name[0] in x]
        print(i, "-", name[0], len(conn), "list: ", conn)

    def takethird(elem):
        return elem[2]

    connection_list.sort(key=takethird, reverse=True)

    return connection_list


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
                if i < len(doc) - 1 and token.pos_ == "PROPN" and doc[i + 1].pos_ == "PROPN":
                    ent = str(token) + " " + str(doc[i + 1])
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
    if STAGE == 1:
        names_list = get_all_alias(entity_list, parsed_list)
        compare_entities([x for x in names_list if len(x) > 1])

        final_list = []
        for entity in names_list:
            if len(entity) == 1:
                final_list.append([entity[0]])
            elif len(entity) == 2:
                if entity[0] == entity[1].split(" ")[0] or entity[0] == entity[1].split(" ")[1]:
                    final_list.append([entity[1]])  # only full name is considered, since it includes the abbreviation
                else:
                    # error
                    final_list.append([entity[0]])
            else:
                list = []
                for i, name in enumerate(entity):
                    if i != 0 and (entity[0] == entity[i].split(" ")[0] or entity[0] == entity[i].split(" ")[1]):
                        list.append([name])
                if list == []:
                    final_list.append([entity[0]])
                else:
                    [final_list.append(x) for x in list]

        # get rid of names including punctuation tokens
        # remove wrong full names
        list = ['Seldon', 'Extinguishing', 'Foundation', 'Field']
        for ent in final_list:
            if any([x for x in punctuation_tokens if x in ent[0]]):
                final_list.remove(ent)
            name = ent[0].split(" ")
            if len(name) == 2 and name[0] in list:
                print(ent)
                final_list.remove(ent)

    else:
        final_list = [['Arkady Darell'], ['Hari Seldon'], ['Seldon Crisis'], ['Raven Seldon'], ['Ducem Barr'],
                      ['Onum Barr'], ['Bayta Darell'], ['Hober Mallow'], ['Trader Mallow'], ['Flober Mallow'], ['Fie'],
                      ['Salvor Hardin'], ['Toran Darell'], ['Gaal Dornick'], ['Pelleas Anthor'], ['Stettin'],
                      ['Ebling Mis'], ['Dorwin'], ['Bail Channis'], ['Homir Munn'], ['Flomir Munn'], ['Han Pritcher'],
                      ['Flan Pritcher'], ['General Pritcher'], ['Mule'], ['First Speaker'], ['Arcadia Darell'],
                      ['Brodrig'], ['Pirenne'], ['Jorane Sutt'], ['Tomaz Sutt'], ['Pappa'], ['Randu'],
                      ['Magnifico Giganticus'], ['Indbur'], ['Jole Turbor'], ['Poly Verisof'], ['Wienis'],
                      ['Limmar Ponyets'], ['Ankor Jael'], ['Sennett Forell'], ['Sef Sermak'], ['Lepold I'],
                      ['Eskel Gorov'], ['Callia'], ['Mayor Hardin'], ['Jord Fara'], ['Grand Master'], ['Master Trader'],
                      ['Bel Riose'], ['Fran'], ['Kleise'], ['Mamma'], ['Yohan Lee'], ['Lee Senter'], ['Lewis Bort'],
                      ['Pherl'], ['Linge Chen'], ['Walto'], ['Theo Aporat'], ['Fox'], ['Elders'], ['Student'],
                      ['Elvett Semic'], ['Avakim'], ['Advocate'], ['Lameth'], ['Yate Fulham'], ['Galactic Empire'],
                      ['Second Empire'], ['First Empire'], ['Orsy'], ['Second Foundation'], ['First Foundation'],
                      ['Encyclopedia Foundation'], ['Personal Capsule'], ['Iwo'], ['Mangin'], ['Ovall Gri'], ['Hella'],
                      ['Jord Commason'], ['Plan'], ['Lev Meirus'], ['Poochie'], ['Preem Palver']]

    print("NER finished:", len(final_list), "'person' entities found")
    return final_list



def ner_event(doc):
    """
    Fact analyses
    Most events are build around patterns of the form: <OBJECT> <VERB> <SUBJECT>
    #TODO: see course 5 slide 35
    """
    subject = ""
    direct_object = ""
    indirect_object = ""
    verb = ""
    # get token dependencies
    for word in doc:
        # subject would be
        if word.dep_ == "nsubj":
            subject = word.orth_
        # iobj for indirect object
        elif word.dep_ == "iobj":
            indirect_object = word.orth_
        # dobj for direct object
        elif word.dep_ == "dobj":
            direct_object = word.orth_
        elif word.dep_ == 'ROOT':
            verb = word
    if str(subject) != "" and str(verb) != "" and str(direct_object) != "":
        print("----------Event---------\n - '", doc.text, "'\n - Who? ", subject, "\n - What?: ", verb, "\n - vs Who? ",
              direct_object, "\n - indirect object: ", indirect_object)
