"""
Given a text and a list of entities (post NER) find all connections between them
"""
from config import *
from cr import coreference_resolution


def family_links(entity_list, connection_list):
    """
    family connections by surname \n
    :return: List of connected entities by surname
    """

    for subset in combinations(entity_list, 2):
        name1 = str(subset[0][0]).split(" ")
        name2 = str(subset[1][0]).split(" ")
        if len(name1) > 1 and len(name2) > 1 and name1[1] == name2[1]:
            connection_list.append([subset[0], subset[1], 1])

    return connection_list


def link_entities(connection_list, entity1, entity):
    """
    Creates link betweeen two entities if conditions apply
    :returns: new link list
    """
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


def solve_coreferences(candidates, token_list, entity_list, pos_current_token):
    """
    Solve coreferences
    :param candidates: list of entities
    :param token_list:
    :param entity_list:
    :param pos_current_token:
    :return:
    """
    if len(candidates) > 1:
        # check if token is surname
        name = token_list[pos_current_token - 1]
        entity2 = entity_from_token(entity_list, name)

        if len(entity2) == 1:
            entity = entity2[0]
        else:
            #ToDo: Coreference resolution
            # Example: token = 'Seldon', get correct candidate from entity_list
            # https://towardsdatascience.com/how-to-make-an-effective-coreference-resolution-model-55875d2b5f19
            # https://neurosys.com/article/most-popular-frameworks-for-coreference-resolution/
            entity = coreference_resolution(candidates, token_list[pos_current_token - 100:pos_current_token + 100])
    else:
        entity = candidates[0]

    return entity


def entity_from_token(entity_list, token):
    return [x for x in entity_list for word in str(x[0]).split(" ") if str(token) == word]


def token_is_candidate(token):
    """
    :return: True if token is proper name or adjective
    """
    if token.pos_ == 'PROPN' or token.pos_ == 'ADJ':
        return True
    else:
        return False


def find_entity_links(entity_list, parsed_list):
    """
    For each entity
        For each sentence in text
            if entity is in sentence
    :return: a list of tuples
    """
    connection_list = []
    connection_list = family_links(entity_list, connection_list)

    token_list = [y for sent in parsed_list for y in sent]
    for i in tqdm(range(len(token_list))):

        token = token_list[i]
        if token_is_candidate(token):
            entity = entity_from_token(entity_list, token)

            if len(entity) > 0:

                # Solve coreferences if more than one candidate
                entity = solve_coreferences(entity, token_list, entity_list, i)

                # find possible entities within the next 35 words
                candidates = [x for x in token_list[i+1:i+35] if token_is_candidate(x)]
                candidates = list(set(candidates))

                # if any of the candidates corresponds to an entity, add connection
                for cand in candidates:
                    entity2 = entity_from_token(entity_list, cand)
                    if len(entity2) > 0:
                        # Solve coreferences if more than one candidate
                        entity2 = solve_coreferences(entity2, token_list, entity_list, i)
                        connection_list = link_entities(connection_list, entity2, entity[0])

    connection_list = print_results_and_sort(entity_list, connection_list)

    return connection_list


def print_results_and_sort(entity_list, connection_list):
    for i, name in enumerate(entity_list):
        conn = [x for x in connection_list if name[0] in x]
        print(i, "-", name[0], len(conn), "list: ", conn)

    def takethird(elem):
        return elem[2]
    connection_list.sort(key=takethird, reverse=True)

    return connection_list
