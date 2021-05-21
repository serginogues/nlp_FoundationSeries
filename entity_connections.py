"""
Given a text and a list of entities (post NER) find all connections between them
"""
from config import combinations
from utils import get_ents_from_doc, pairwise, read_list, write_list


def alias_resolution(list):
    if any(list):
        return list[0]
    else:
        return None


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


def link_two_person(connection_list, entity1, entity, idx_sent):
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
            connection_list.append([entity1, entity, 1, idx_sent])

    return connection_list


def entity_links(people_list, location_list, parsed_list, STAGE=True):
    """
    Two entities are considered to have a link if they appear in a range of two consecutive sentences.
    :return: a list of tuples
    """
    if STAGE:
        people_links = []
        location_links = []
        idx_sentence = 0  # sum(1 for _ in c)
        for pair in pairwise(parsed_list):
            ents_list = get_ents_from_doc(pair[0]) + get_ents_from_doc(pair[1])
            ents_list = list(set(ents_list))
            if any(ents_list):

                # PEOPLE
                people = entity_candidates(ents_list, people_list)
                for a, b in combinations(people, 2):
                    people_links = link_two_person(people_links, a, b, idx_sentence)

                # LOCATIONS
                locations = location_candidates(ents_list, location_list)
                if any(locations) and any(people):
                    for loc in locations:
                        for pers in people:
                            if pers != loc:
                                location_links.append([loc, pers, idx_sentence])
                    print(locations, people, "in sentence:", " ".join([parsed_list[idx_sentence].text, parsed_list[idx_sentence+1].text]))

            idx_sentence += 1

        # POST PROCESS
        people_links = sorted([x for x in people_links if x[2] > 2], key=lambda x: x[2], reverse=True)
        people_links = [x for x in people_links if x[2] > 4]
        write_list('people_links', people_links)
        write_list('location_links', location_links)

    else:
        people_links = read_list('people_links')
        location_links = read_list('location_links')

    return people_links, location_links


def entity_candidates(ents_list, entity_list):
    candidates = []
    for ent in ents_list:
        candidates += [x[0] for x in entity_list for name in x if name == ent]
    candidates = list(set(candidates))
    return candidates


def location_candidates(ents_list, entity_list):
    candidates = []
    for ent in ents_list:
        candidates += [x for x in entity_list if ent == x]
    candidates = list(set(candidates))
    return candidates
