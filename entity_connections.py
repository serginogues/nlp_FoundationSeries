"""
Given a text and a list of entities (post NER) find all connections between them
"""
from config import combinations, nlp
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


def link_two_person(connection_list, entity1, entity):
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


def LINK_ENTITIES(parsed_list, predicted, STAGE=True):
    """
    Two entities are considered to have a link if they appear in a range of two consecutive sentences.
    :return: a list of tuples
    """
    if STAGE:
        people_links = []
        per_link = []
        location_links = []

        for idx in range(len(parsed_list)):
            per, loc, per_idx, loc_idx = get_ents_from_predicted(predicted[idx], parsed_list[idx])
            if idx < len(parsed_list) - 1:
                per2, loc2, per_idx2, loc_idx2 = get_ents_from_predicted(predicted[idx+1], parsed_list[idx+1])
                per += per2
                loc += loc2
                per_idx += per_idx2
                loc_idx += loc_idx2
            per = list(set(per))
            loc = list(set(loc))

            # PEOPLE
            for a, b in combinations(per, 2):
                link_two_person(people_links, a, b)
                per_link.append([a, b, idx])

            # LOCATIONS
            if any(loc) and any(per):
                for l in loc:
                    for p in per:
                        if p != l:
                            location_links.append([l, p, idx])

        # POST PROCESS
        people_links = sorted([x for x in people_links if x[2] > 2], key=lambda x: x[2], reverse=True)
        write_list('people_links', people_links)
        write_list('location_links', location_links)

    else:
        people_links = read_list('people_links')
        location_links = read_list('location_links')

    return people_links, location_links


def coref_events(doc, people_list, location_list, idx):
    """
    https://ryanong.co.uk/2020/07/14/day-196-coreference-resolution-with-neuralcoref-spacy/
    """
    event_links = []
    for token in doc:
        if token._.has_coref:
            print(token._.coref_cluster)
    return event_links


def get_ents_from_predicted(y_pred, doc):
    """
    :param predicted: ner output
    :param doc: spacy doc
    :return:
    """
    per = []
    loc = []
    per_idx = []
    loc_idx = []
    for i, name in [(i, tag) for i, tag in enumerate(y_pred) if tag != 'O']:
        if name == 'B-PER':
            per.append(doc[i].text)
            per_idx.append(i)
        elif name == 'I-PER':
            per[-1] = " ".join([per[-1], doc[i].text])
            per_idx[-1] = i
        if name == 'B-LOC':
            loc.append(doc[i].text)
            loc_idx.append(i)
        elif name == 'I-LOC':
            loc[-1] = " ".join([loc[-1], doc[i].text])
            loc_idx[-1] = i

    return per, loc, per_idx, loc_idx


