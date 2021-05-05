from itertools import islice
from cr import coreference_resolution
from preprocess import *

"""
https://dh2016.adho.org/abstracts/297
The first network is based on co-occurrences of characters in the same window of text: 
an edge between two characters exists if they are mentioned in the same paragraph and the weight of the edge is 
the number of paragraphs in which this is the case.
"""


def family_links(entity1, entity2):
    """
    :return: True if entity1 and 2 share the same surname
    """
    print("hey")


def check_exist(connection_list, entity1, entity):
    if entity1 != entity:
        found = False
        for link in connection_list:
            a = False
            b = False
            for i, ent in enumerate(link):
                if i != 2 and entity1 == ent:
                    a = True
                if i != 2 and entity == ent:
                    b = True
            if a and b:
                link[2] += 1
                found = True

        if not found:
            connection_list.append([entity1, entity, 1])

    return connection_list


def first_or_second(entity1, entity, count, connection_list, span):
    # found entity
    # first or second entity?
    if entity1 is None:
        # first
        entity1 = entity
    else:
        if count < 35:
            # second
            connection_list = check_exist(connection_list, entity1, entity)
            #print("******Found connection between -", entity1, "- and -", entity, "*****************")
            #print("Sentence: \n", span)
        # first
        entity1 = entity
        count = 0

    return entity1, count, connection_list


def find_entity_links(entity_list, parsed_list):
    """
    For each entity
        For each sentence in text
            if entity is in sentence
    :return: a list of tuples
    """
    connection_list = []

    # family connections
    for subset in combinations(entity_list, 2):
        name1 = str(subset[0][0]).split(" ")
        name2 = str(subset[1][0]).split(" ")
        if len(name1) > 1 and len(name2) > 1 and name1[1] == name2[1]:
            connection_list.append([subset[0], subset[1], 1])

    # 0 - preprocessing


    token_list = [y for sent in parsed_list for y in sent]
    for i in tqdm(range(len(token_list))):
        token = token_list[i]
        if token.pos_ == 'PROPN' or token.pos_ == 'ADJ':
            entity = [x for x in entity_list for word in str(x[0]).split(" ") if str(token) == word]

            # region Deprecated
            """for ent in entity_list:
                for alias in ent:
                    full_entity_name = str(alias).split(" ")  # "Hari Seldon" -> ["Hari", "Seldon"]
                    if len(full_entity_name) == 1 and str(token) == str(alias):
                        # candidate has only name
                        entity.append(ent)
                        break
                    elif len(full_entity_name) > 1 and str(token) == full_entity_name[0] and str(token_list[i + 1]) == \
                            full_entity_name[1]:
                        entity.append(ent)
                        break
                    elif len(full_entity_name) > 1 and str(token) == full_entity_name[1]:
                        entity.append(ent)
                        break"""
            #endregion

            #ToDo: Coreference resolution
            # Example: token = 'Seldon', get correct candidate from entity_list
            # https://towardsdatascience.com/how-to-make-an-effective-coreference-resolution-model-55875d2b5f19
            # https://neurosys.com/article/most-popular-frameworks-for-coreference-resolution/
            if len(entity) > 0:

                if len(entity) > 1:
                    # check if its surname
                    entity2 = [x for x in entity_list for word in str(x[0]).split(" ") if str(token_list[i-1]) == word]

                    if len(entity2) == 0 or len(entity2) > 1:
                        # need to do CR
                        entity = coreference_resolution(entity, token_list[i-10:i+10])
                    else:
                        entity = entity2[0]
                else:
                    entity = entity[0]


                candidates = [x for x in token_list[i+1:i+35] if x.pos_ == 'PROPN' or x.pos_ == 'ADJ']
                candidates = list(set([x.text for x in candidates]))

                for cand in candidates:
                    link = [x for x in entity_list for word in str(x[0]).split(" ") if str(cand) == word]
                    if len(link) > 0:
                        link = coreference_resolution(link, token_list[i-10:i+10])
                        connection_list = check_exist(connection_list, link[0], entity[0])

    for i, name in enumerate(entity_list):
        conn = [x for x in connection_list if name[0] in x]
        print(i, "-", name[0], len(conn), "list: ", conn)

    def takethird(elem):
        return elem[2]
    connection_list.sort(key=takethird, reverse=True)

    return connection_list
